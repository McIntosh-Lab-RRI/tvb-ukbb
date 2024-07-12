#!/bin/env python
#
# Script name: consistency_thresholding.py
#
#

# Description: Script to consistency threshold a group of processed subjects' structural
# connectivity matrices.
#
#
# Usage: python consistency_thresholding.py <zip_dir> <threshold> <subject_list> <PARC_NAME>
#
# NOTE: existing tvb_inputs.zip file names should follow the following format:

#
#                    subjectName_parcellationName_tvb_inputs.zip
#
#
# Parameters:   zip_dir         -   path to directory containing tvb_inputs.zip files for all
#                               subjects to be consistency thresholded
#
#               threshold       -   float representing rate at which each structural connection
#                               should appear (have a non-zero probability of connection) in the
#                               group of subjects. (e.g. threshold=0.4 will eliminate any
#                               connections, from all subjects, that dont appear in at least 40% of
#                               subjects)
#
#               subject_list    -   path to text file containing subject names, one per line, to be
#                               thresholded
#
#               PARC_NAME       -   name of parcellation. use "" if these zip files were created
#                               with an earlier version of the pipeline that did not specify
#                               parcellations in tvb_input.zip filenames
#
#
# Output: new thresholded_tvb_inputs directory in zip_dir, containing all subjects' new
# tvb_inputs.zip files with newly thresholded weights.txt (SC matrix files)
#
#
## Author: Justin Wang

import numpy as np
import sys
import os
import zipfile
import shutil
import csv
from connectivity_correlation import connectivity_correlation
import math
import matplotlib.pyplot as plt



def ED_TL_correlation(
    zip_dir, subject_list, PARC_NAME, PARC_LUT, subject_age_list_file
):
    """Script to consistency threshold a group of processed subjects' structural
     connectivity matrices.


    Arguments
    ----------

    zip_dir :
        path to directory containing tvb_inputs.zip files for all
        subjects to be consistency thresholded

    threshold :
        float representing rate at which each structural connection
        should appear (have a non-zero probability of connection) in the
        group of subjects. (e.g. threshold=0.4 will eliminate any
        connections, from all subjects, that dont appear in at least 40% of
        subjects)

    subject_list :
        path to text file containing subject names, one per line, to be
        thresholded

    PARC_NAME :

        name of parcellation. use "" if these zip files were created
        with an earlier version of the pipeline that did not specify
        parcellations in tvb_input.zip filenames

    """


    # make output dir
    outputdir = os.path.join(zip_dir, "ED_TL_matrices")
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    # import subject names into subjects array
    subjects = []
    with open(subject_list) as subject_list_file:
        for line in subject_list_file:
            line = line.rstrip("\n")
            subjects.append(line)

    # open PARC_LUT int ROI_list
    datafile = open(PARC_LUT, "r")
    datareader = csv.reader(datafile, delimiter="\t")
    ROI_list = []

    for row in datareader:
        row[0] = int(row[0])
        ROI_list.append(row)

    # IF ED TL files dont exist already in outputdir, gen them
    # unzip each subject into output dir
    for subject in subjects:
        # source zip name
        subject_file_name = ""
        # path to source zip
        subject_zip = ""

        # different source zip name and path if PARC_NAME present

        subject_file_name = subject + "_" + PARC_NAME + "_tvb_inputs.zip"
        subject_zip = os.path.join(zip_dir, subject_file_name)

        # gen EDTL files if the subj zip is available
        if os.path.exists(subject_zip):
            # uncompressed tvb input folder location (in outputdir)
            uncompressed_subj = os.path.join(outputdir, subject_file_name[:-4])

            # if ED and TL txt files for this sub and parc dont both exist in outputdir,
            if not (
                os.path.exists(uncompressed_subj[:-10] + "ED.txt")
                and os.path.exists(uncompressed_subj[:-10] + "TL.txt")
            ):
                # unzip into outputdir
                with zipfile.ZipFile(subject_zip, "r") as zip_ref:
                    zip_ref.extractall(outputdir)

                # struct zip
                struct_zip = os.path.join(uncompressed_subj, "structural_inputs.zip")

                # unzip struct zip
                if os.path.exists(struct_zip):
                    with zipfile.ZipFile(struct_zip, "r") as zip_ref:
                        zip_ref.extractall(uncompressed_subj)

                    TL_path = os.path.join(struct_zip[:-4], "tract_lengths.txt")
                    centres_path = os.path.join(struct_zip[:-4], "centres.txt")

                    # load TL and save into outputdir
                    TL = ""
                    if os.path.exists(TL_path):
                        TL = np.loadtxt(TL_path)
                        np.savetxt(uncompressed_subj[:-10] + "TL.txt", TL)

                    # load centres and save ED matrix into outputdir
                    centres = ""
                    if os.path.exists(centres_path):
                        centres = np.genfromtxt(centres_path, dtype="str")
                        ED = np.zeros((centres.shape[0], centres.shape[0]))
                        for i in range(centres.shape[0]):
                            for j in range(centres.shape[0]):
                                a = np.array(
                                    (
                                        float(centres[i][1]),
                                        float(centres[i][2]),
                                        float(centres[i][3]),
                                    )
                                )
                                b = np.array(
                                    (
                                        float(centres[j][1]),
                                        float(centres[j][2]),
                                        float(centres[j][3]),
                                    )
                                )
                                ED[i][j] = np.linalg.norm(a - b)

                        np.savetxt(uncompressed_subj[:-10] + "ED.txt", ED)

                # remove uncompressed subj from outputdir
                shutil.rmtree(uncompressed_subj)

    ED_array = ""
    TL_array = ""
    sub_array = ""
    decile_array = ""

    subject_age_list = np.genfromtxt(subject_age_list_file, dtype="str")

    # go through subjects and populate arrays, one index per subj
    for index, subject in enumerate(subjects):  #
        # load ED, TL
        ED_file = subject + "_" + PARC_NAME + "_ED.txt"
        TL_file = subject + "_" + PARC_NAME + "_TL.txt"

        if (
            os.path.exists(os.path.join(outputdir, ED_file))
            and os.path.exists(os.path.join(outputdir, TL_file))
            and os.path.exists(subject_age_list_file)
        ):
            ED = np.loadtxt(os.path.join(outputdir, ED_file))
            TL = np.loadtxt(os.path.join(outputdir, TL_file))
            decile = np.nan
            decile = float(
                [
                    item[1]
                    for i, item in enumerate(subject_age_list)
                    if subject in item[0]
                ][0]
            )
            if not math.isnan(decile):
                decile = math.floor(decile / 10)

            if index == 0:
                ED_array = np.array([ED])
                TL_array = np.array([TL])
                sub_array = np.array([subject])
                decile_array = np.array([decile])

            else:
                ED_array = np.append(ED_array, np.array([ED]), axis=0)
                TL_array = np.append(TL_array, np.array([TL]), axis=0)
                sub_array = np.append(sub_array, np.array([subject]), axis=0)
                decile_array = np.append(decile_array, np.array([decile]), axis=0)

        else:
            print(subject, "missing ED or TL")

    # create 2d list of deciles containing [age, whole brain EDTL correlation]
    whole_brain_EDTL = []
    for i in range(ED_array.shape[0]):
        # print(connectivity_correlation(ED_array[i],TL_array[i],False))
        # print(connectivity_correlation(ED_array[i],TL_array[i],False)[0])
        # print(decile_array[i])

        whole_brain_EDTL.append(
            [
                decile_array[i],
                connectivity_correlation(ED_array[i], TL_array[i], False)[0],
            ]
        )

    whole_brain_EDTL = np.array(whole_brain_EDTL)
    deciles = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # get

    x = []
    # create list for each decile
    for decile in deciles:
        mylist = whole_brain_EDTL[whole_brain_EDTL[:, 0] == decile][:, 1]
        x.append(mylist)
        print(
            str(decile), " decile average EDTL correlation: ", str(np.average(mylist))
        )
    plt.boxplot(x)
    plt.title("Whole-Brain Euclidean Distance - Tract Length Matrix Correlation")
    plt.xlabel("Decile")
    plt.ylabel("Whole-Brain ED-TL Pearson Correlation")

    plt.savefig(os.path.join(outputdir, "ED_TL_wholebrain_by_decile.png"), format="png")
    plt.savefig(os.path.join(outputdir, "ED_TL_wholebrain_by_decile.svg"), format="svg")

    plt.show()
    # whole brain edtl vis:
    # average of all correlations, as well as by decile


if __name__ == "__main__":
    """Script to consistency threshold a group of processed subjects' structural
     connectivity matrices.


    Usage
    ----------
    python consistency_thresholding.py <zip_dir> <threshold> <subject_list> <PARC_NAME>


    Arguments
    ----------
    zip_dir :
        path to directory containing tvb_inputs.zip files for all
        subjects to be consistency thresholded

    threshold :
        float representing rate at which each structural connection
        should appear (have a non-zero probability of connection) in the
        group of subjects. (e.g. threshold=0.4 will eliminate any
        connections, from all subjects, that dont appear in at least 40 percent of
        subjects)

    subject_list :
        path to text file containing subject names, one per line, to be
        thresholded

    PARC_NAME :

        name of parcellation. use "" if these zip files were created
        with an earlier version of the pipeline that did not specify
        parcellations in tvb_input.zip filenames

    """
    # try:

    ED_TL_correlation(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
