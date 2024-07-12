#!/bin/env python
#
# Script name: IDP_html_gen.py
#
# Description: Script to generate IDP page of QC html report.
#
## Author: Justin Wang

import pandas as pd
import numpy as np
import sys
import os
from ast import literal_eval


def formatter(x):
    try:
        return "{:e}".format(float(x))
    except:
        return x


def generate_full_IDPoi_data(df, IDP_dir):
    """Function that adds IDP values to an existing IDP dataframe, using the
    relevant IDP txt from the subject's IDP directory. Each IDP txt file
    corresponds with a IDP category.


    Parameters
    ----------
    df : pd.DataFrame
        Dataframe containing details about IDPs, no values present.
    IDP_dir : string
        Full path to the directory containing the subject's IDP output
        txt files.


    Returns
    ----------
    output : pd.DataFrame
        Dataframe containing details about IDPs, with values included
    """

    flag = False
    # output df placeholder
    output = pd.DataFrame(
        columns=[
            "num",
            "short",
            "category",
            "num_in_cat",
            "long",
            "unit",
            "dtype",
            "description",
            "value",
        ],
    )

    # for each IDP category, access its corresponding IDP value file
    for category in df["category"].unique():
        # sub-df containing only IDPs for this category
        df_sub = df[df["category"] == category]

        # open the caregory's IDP value txt file, clean whitespaces, and split into a df
        cat_data = []
        try:
            with open(IDP_dir + category + ".txt") as my_file:
                for line in my_file:
                    line = line.strip()
                    line = line.split(" ")
                    cat_data.append(line)
            cat_data = pd.DataFrame(cat_data)
            cat_data = cat_data.T
            cat_data.columns = ["value"]
            cat_data["num_in_cat"] = cat_data.index + 1

            cat_data = cat_data.astype({"num_in_cat": int})
            df_sub = df_sub.astype({"num_in_cat": int})

            # inner join the category's IDP values with the sub-df for this category
            df_sub = df_sub.merge(cat_data, how="left", on="num_in_cat")

            # left should work - used to be inner join. now left join to show if there are any missing IDP values

            # if this is the first sub-df, then the output df is the same as the sub-df for now
            # otherwise, append sub-df ot output df
            if not flag:
                output = df_sub
                flag = True
            else:
                output = output.append(df_sub, ignore_index=True)

        except:
            print(IDP_dir + category + ".txt file missing")

    return output


def IDP_postprocessing(subj, IDP_list_path, IDPoi_list_path, thresholds_txt):
    """Function that generates the IDP page of the QC report for a
    subject.

    TODO: remove duplicate code by having a single function used
            twice - once for low-priority and once for high
    TODO: handle missing low-priority lines in the IDPoi
    TODO: separate low and high priority IDPs in report

    Parameters
    ----------
    subj : string
        Full path to subject's directory.
    IDP_list_path : string
        Full path to IDP list (file containing IDP information).
    IDPoi_list_path : string
         Full path to IDPoi list (file containing list of IDPs of interest).
    """

    # remove trailing forward slashes in subject paths
    if subj.endswith("/"):
        subj = subj[:-1]

    QC_dir = subj + "/QC/html/"
    IDP_dir = subj + "/IDP_files/"

    if not os.path.exists(IDP_dir):
        os.makedirs(IDP_dir)

    subjName = subj[subj.rfind("/") + 1 :]

    # reading and cleaning each line of IDP list
    IDP_list = []
    with open(IDP_list_path) as my_file:
        for line in my_file:
            line = line.strip()
            IDP_list.append(line)
    i = 0
    # remove header
    IDP_list = IDP_list[1:]

    # cleaning just in case - should run fine even if data is already clean
    while i < len(IDP_list):
        IDP_list[i] = IDP_list[i].replace('"', "")
        IDP_list[i] = " ".join(IDP_list[i].split())
        IDP_list[i] = " ".join(IDP_list[i].split("\\t"))
        IDP_list[i] = IDP_list[i].split(" ", 7)
        i += 1

    # IDP list dataframe containing details about every IDP
    IDP = pd.DataFrame(
        IDP_list,
        columns=[
            "num",
            "short",
            "category",
            "num_in_cat",
            "long",
            "unit",
            "dtype",
            "description",
        ],
    )

    # reading each line of IDPoi list
    IDPoi_list = []

    with open(IDPoi_list_path) as my_file:
        for line in my_file:
            line = line.strip()
            IDPoi_list.append(line)
    IDPoi = np.array(IDPoi_list)

    # splitting IDPois into high and low priority dataframes
    priority = True
    priority_array = []
    non_priority_array = []
    for line in IDPoi:
        if line == "HIGH_PRIORITY":
            priority = True
        elif line == "LOW_PRIORITY":
            priority = False
        else:
            if priority:
                priority_array.append(line)
            else:
                non_priority_array.append(line)

    priority_df = pd.DataFrame(priority_array, columns=["short"])
    non_priority_df = pd.DataFrame(non_priority_array, columns=["short"])

    # filling details about the IDPs for both priority and non priority IDPoi dfs
    # by merging the dfs with the IDP list dataframe
    # TODO handle IDPoi that dont exist/typoed
    priority_df = priority_df[["short"]]
    priority_df = priority_df.merge(IDP, how="inner", left_on="short", right_on="short")

    non_priority_df = non_priority_df[["short"]]
    non_priority_df = non_priority_df.merge(
        IDP, how="inner", left_on="short", right_on="short"
    )

    # get values for each IDPoi
    # TODO: handle empty IDP values
    priority_output = generate_full_IDPoi_data(priority_df, IDP_dir)
    non_priority_output = generate_full_IDPoi_data(non_priority_df, IDP_dir)

    # retain
    priority_output = priority_output[
        [
            "num",
            "short",
            "category",
            "num_in_cat",
            "long",
            "unit",
            "dtype",
            "description",
            "value",
        ]
    ]

    non_priority_output = non_priority_output[
        [
            "num",
            "short",
            "category",
            "num_in_cat",
            "long",
            "unit",
            "dtype",
            "description",
            "value",
        ]
    ]

    new_IDP_output = pd.read_csv(r"" + IDP_dir + "tvb_new_IDPs.tsv", delimiter="\t")
    # new_IDP_output=new_IDP_output[["num","short","category","num_in_cat","long","unit","dtype","description","value"]]

    # prior, non prior, new tvb IDP compiled output
    last_IDP_num = int(IDP["num"].iloc[-1])
    new_IDP_output["num"] += last_IDP_num
    compiled_IDPs = pd.concat([priority_output, new_IDP_output])
    compiled_IDPs = pd.concat([compiled_IDPs, non_priority_output])

    try:
        # need ot handle missing value as a failure as well
        # filling in threshold values

        failed_IDP = ""

        thresholds = pd.read_csv(thresholds_txt, sep="\t")

        IDPs_with_thresholds = compiled_IDPs.merge(thresholds, how="left", on="short")
        IDPs_with_thresholds["flag"] = ""
        passed_QC_flag = True

        for index, row in IDPs_with_thresholds.iterrows():
            IDP_failed = True

            current_range = row["accepted_ranges"]
            if str(current_range) == "nan" or str(current_range) == "NaN":
                IDPs_with_thresholds.at[index, "flag"] = "N/A"
            # only add flag colours for IDPs which are in the thresholds txt
            else:
                # iterate through ranges
                for x in current_range.split(";"):
                    x = literal_eval(x)
                    if x[0] == "-inf":
                        if row["value"] <= x[1]:
                            IDP_failed = False

                    elif x[1] == "inf":
                        if row["value"] >= x[0]:
                            IDP_failed = False

                    else:
                        if float(row["value"]) >= float(x[0]) and float(
                            row["value"]
                        ) <= float(x[1]):
                            IDP_failed = False
                if IDP_failed:
                    passed_QC_flag = False
                    failed_IDP += "\t" + row["short"] + ":" + str(row["value"])
                    IDPs_with_thresholds.at[index, "flag"] = IDP_failed

        if not passed_QC_flag:
            failed_IDP = subj + failed_IDP
            f = open(os.path.join(os.path.dirname(subj), "IDP_flags.txt"), "a")
            f.write(failed_IDP + "\n")
            f.close()

        # print(IDPs_with_thresholds)

        # return values back to scientific notation
        priority_output["num"] = priority_output["num"].astype(np.int64)
        non_priority_output["num"] = non_priority_output["num"].astype(np.int64)
        compiled_IDPs["num"] = compiled_IDPs["num"].astype(np.int64)
        IDPs_with_thresholds["num"] = IDPs_with_thresholds["num"].astype(np.int64)
        new_IDP_output["num"] = new_IDP_output["num"].astype(np.int64)

        # new_IDP_output['value'] = new_IDP_output['value'].apply(lambda x: "{:e}".format(float(x)))
        # IDPs_with_thresholds['value'] = IDPs_with_thresholds['value'].apply(lambda x: "{:e}".format(float(x)))

        try:
            # merging with threshold information
            priority_output["value"] = priority_output["value"].astype(str)
            non_priority_output["value"] = non_priority_output["value"].astype(str)
            compiled_IDPs["value"] = compiled_IDPs["value"].astype(str)
            new_IDP_output["value"] = new_IDP_output["value"].astype(str)
            IDPs_with_thresholds["value"] = IDPs_with_thresholds["value"].astype(str)

            priority_output = priority_output.merge(
                IDPs_with_thresholds,
                how="left",
                on=[
                    "num",
                    "short",
                    "category",
                    "num_in_cat",
                    "long",
                    "unit",
                    "dtype",
                    "description",
                    "value",
                ],
            )
            non_priority_output = non_priority_output.merge(
                IDPs_with_thresholds,
                how="left",
                on=[
                    "num",
                    "short",
                    "category",
                    "num_in_cat",
                    "long",
                    "unit",
                    "dtype",
                    "description",
                    "value",
                ],
            )
            compiled_IDPs = compiled_IDPs.merge(
                IDPs_with_thresholds,
                how="left",
                on=[
                    "num",
                    "short",
                    "category",
                    "num_in_cat",
                    "long",
                    "unit",
                    "dtype",
                    "description",
                    "value",
                ],
            )

            # try:
            # IDPs_with_thresholds["value"] = IDPs_with_thresholds.value.astype(float)
            new_IDP_output = new_IDP_output.merge(
                IDPs_with_thresholds,
                how="left",
                on=[
                    "num",
                    "short",
                    "category",
                    "num_in_cat",
                    "long",
                    "unit",
                    "dtype",
                    "description",
                    "value",
                ],
            )
            # except:
            #     print("ERROR: merge issue between new IDP and thresholded IDPs")

            # scientific notation for values
            priority_output["value"] = priority_output["value"].apply(formatter)
            non_priority_output["value"] = non_priority_output["value"].apply(formatter)
            new_IDP_output["value"] = new_IDP_output["value"].apply(formatter)
            compiled_IDPs["value"] = compiled_IDPs["value"].apply(formatter)
        except:
            print("ERROR: merging or formatting error")

        # save IDPois to txt files for future reference
        priority_output.to_csv(
            r"" + IDP_dir + "priority_IDPs.tsv",
            header=priority_output.columns.values,
            index=None,
            sep="\t",
            mode="w",
        )
        non_priority_output.to_csv(
            r"" + IDP_dir + "non_priority_IDPs.tsv",
            header=non_priority_output.columns.values,
            index=None,
            sep="\t",
            mode="w",
        )
        compiled_IDPs.to_csv(
            r"" + IDP_dir + "significant_IDPs.tsv",
            header=compiled_IDPs.columns.values,
            index=None,
            sep="\t",
            mode="w",
        )
        new_IDP_output.to_csv(
            r"" + IDP_dir + "tvb_new_IDPs.tsv",
            header=compiled_IDPs.columns.values,
            index=None,
            sep="\t",
            mode="w",
        )

    except:
        print("Error: thresholds or merging error")
    # need to save each txt priority txt again with merge to include flags and the threshold
    # need to gen colour based of flag and presence of threshold


if __name__ == "__main__":
    """Function that adds IDP values to an existing IDP dataframe, using the
    relevant IDP txt from the subject's IDP directory. Each IDP txt file
    corresponds with a IDP category.


    Usage
    ----------
    python  IDP_html_gen.py  subj  IDP_list_path  IDPoi_list_path


    Arguments
    ----------
    subj :
        Full path to subject's directory.

    IDP_list_path :
        Full path to IDP list (file containing IDP information).
        ukbb_IDP_list.txt
        IDP list is a tab delimited file with columns:  "num",
                                                        "short",
                                                        "category",
                                                        "num_in_cat",
                                                        "long",
                                                        "unit",
                                                        "dtype",
                                                        "description"
    IDPoi_list_path :
        Full path to IDPoi list (file containing list of IDPs of interest).
        IDPoi file must contain a line with "HIGH PRIORITY" followed by
        shortform IDP names (one per line) that are high priority. Any
        low priority IDPs should follow (one per line) a new line
        with "LOW PRIORITY".

    """
    # try:
    IDP_postprocessing(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
