#!/bin/env python

import pandas as pd
import numpy as np
import sys
import os
import csv


def ukbb_IDP_list_gen(BB_BIN_DIR, PARC_LUT):
    """Function that updates the ukbb_IDP_list txt file
    Parameters
    ----------
    BB_BIN_DIR: path to tvb pipeline tvb-ukbb

    PARC_LUT: path to LUT.txt

    """
    # grab PARC_LUTs and generate IDP information for each ROI
    ROI_data = list(
        csv.reader(
            open(PARC_LUT),
            delimiter="\t",
        )
    )
    i = 1
    for row in ROI_data:
        row[1] = "T1_GM_parcellation_" + row[1] + "_vol"
        row.append("bb_IDP_T1_GM_parcellation")
        row.append(i)
        row.append("T1_GM_parcellation_" + row[1] + "_volume")
        row.append("mm3")
        row.append("float")
        row.append("Volume of grey matter in " + row[1] + " (From T1 brain image)")
        i = i + 1

    # reading and cleaning each line of IDP list
    IDP_list = []
    IDP_list_path = os.path.join(BB_BIN_DIR, "bb_IDP", "ukbb_IDP_list.tsv")

    data = list(
        csv.reader(
            open(IDP_list_path),
            delimiter="\t",
        )
    )
    on_GM = False
    start = len(data)
    end = len(data)
    found_T2_WMH = False
    for x in range(len(data)):
        if found_T2_WMH == False:
            if data[x][2] == "bb_IDP_T2_FLAIR_WMH":
                found_T2_WMH = x

        if on_GM == False:
            if data[x][2] == "bb_IDP_T1_GM_parcellation":
                start = x
                on_GM = True
        else:
            if data[x][2] != "bb_IDP_T1_GM_parcellation":
                end = x
                on_GM = False

    if start == len(data):
        # no GM parcellation IDPs in here. just append to found_T2_WMH
        if found_T2_WMH == False:
            for index in range(len(ROI_data)):
                data.append(ROI_data[index])
            # append to end if there is no T2 WMH IDP
        else:
            indexes_to_insert = range(len(ROI_data))
            for index in sorted(indexes_to_insert, reverse=True):
                data.insert(found_T2_WMH, ROI_data[index])
            # insert in found_T2_WMH and push back
    else:
        indexes_to_delete = range(start, end)
        for index in sorted(indexes_to_delete, reverse=True):
            del data[index]  # erase and insert where found
        indexes_to_insert = range(len(ROI_data))
        for index in sorted(indexes_to_insert, reverse=True):
            data.insert(start, ROI_data[index])

    #
    x = 1
    for row in data[1:]:
        row[0] = x
        x = x + 1

    with open(IDP_list_path, mode="w") as outputfile:
        writer = csv.writer(outputfile, delimiter="\t")

        writer.writerows(data)


if __name__ == "__main__":
    """Function that updates the ukbb_IDP_list txt file.


    Usage
    ----------
    python  IDP_html_gen.py  IDP_list_path


    Arguments
    ----------


    BB_BIN_DIR: path to tvb pipeline tvb-ukbb


    PARC_LUT: path to LUT.txt


    """
    # try:
    ukbb_IDP_list_gen(sys.argv[1], sys.argv[2])
