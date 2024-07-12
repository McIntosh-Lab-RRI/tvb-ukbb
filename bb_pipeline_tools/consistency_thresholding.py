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



def consistency_thresholding(
    zip_dir, threshold, subject_list, PARC_NAME, PARC_LUT, ROI_remove
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
    outputdir = os.path.join(zip_dir, "thresholded_tvb_inputs")
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    # import subject names into an array
    subjects = []
    with open(subject_list) as subject_list_file:
        for line in subject_list_file:
            line = line.rstrip("\n")
            subjects.append(line)

    # import ROIs to remove into an array
    ROIs_to_remove = []
    with open(ROI_remove) as ROI_remove_file:
        for line in ROI_remove_file:
            line = line.rstrip("\n")
            ROIs_to_remove.append(line)

    # open PARC_LUT
    datafile = open(PARC_LUT, "r")
    datareader = csv.reader(datafile, delimiter="\t")
    ROI_list = []

    for row in datareader:
        row[0] = int(row[0])
        ROI_list.append(row)

    # change ROIs_to_remove from list of ROI #s to remove into list of matrix indices to remove
    for i in range(len(ROIs_to_remove)):
        for j in range(len(ROI_list)):
            if int(ROIs_to_remove[i]) == int(ROI_list[j][0]):
                ROIs_to_remove[i] = j


    consistency_mask = ""
    subcounter = 0

    # unzip each subject into output dir
    for subject in subjects:
        # source zip name
        subject_file_name = ""
        # path to source zip
        subject_zip = ""

        # different source zip name and path if PARC_NAME present
        if PARC_NAME == "":
            subject_file_name = subject + "_tvb_inputs.zip"
            subject_zip = os.path.join(zip_dir, subject_file_name)
        else:
            subject_file_name = subject + "_" + PARC_NAME + "_tvb_inputs.zip"
            subject_zip = os.path.join(zip_dir, subject_file_name)

        # unzip subject
        if os.path.exists(subject_zip):
            with zipfile.ZipFile(subject_zip, "r") as zip_ref:
                zip_ref.extractall(outputdir)

            # past version of pipeline generates SUBJECTNAME_tvb_inputs.zip, but once uncompressed, the resulting tvb_inputs dir not have SUBJECTNAME in the filename.
            # if name of uncompressed dir from this subj zip is ambiguous, give it a better name
            ambiguous_dir = os.path.join(outputdir, "tvb_inputs")
            specific_dir = os.path.join(outputdir, subject_file_name[:-4])

            # rename uncompressed zip
            if os.path.exists(ambiguous_dir):
                os.rename(ambiguous_dir, specific_dir)

            end_dir = specific_dir

            # past version of pipeline generates SUBJECTNAME_tvb_structural_inputs.zip within the tvb_inputs directory.
            # new version generates structural_inputs.zip instead
            specific_struct_zip = os.path.join(
                end_dir, subject + "_tvb_structural_inputs.zip"
            )
            ambiguous_struct_zip = os.path.join(end_dir, "structural_inputs.zip")

            if os.path.exists(specific_struct_zip):
                os.rename(specific_struct_zip, ambiguous_struct_zip)

            # unzip struct inputs
            struct_zip = ambiguous_struct_zip

            with zipfile.ZipFile(struct_zip, "r") as zip_ref:
                zip_ref.extractall(end_dir)

            # path to SC
            SC_path = os.path.join(end_dir, "structural_inputs", "weights.txt")

            SC = ""
            if os.path.exists(SC_path):
                # load SC
                SC = np.loadtxt(SC_path)

                # remove ROIs from SC and save without these ROIs
                SC = np.delete(SC, ROIs_to_remove, axis=0)
                SC = np.delete(SC, ROIs_to_remove, axis=1)
                np.savetxt(SC_path, SC)

                if np.any(np.isnan(SC)):

                    print("found nan in", SC_path)
                else:
                    # binarize SC and add to consistency mask to track how many subs have a connnection for each connection
                    SC = np.where(SC > 0, 1, 0)
                    if consistency_mask == "":
                        consistency_mask = SC
                    else:
                        consistency_mask = consistency_mask + SC
                    subcounter = subcounter + 1

            # delete dir if ambiguous (this code shouldnt run anyway)
            if os.path.exists(ambiguous_dir):
                shutil.rmtree(ambiguous_dir)

    # quit if weve encountered no nan-less SC matrices
    if consistency_mask == "":
        quit()

    # binarize consistency mask, thresholded by (#subs * threshold %)
    min_sub_count = float(threshold) * subcounter
    consistency_mask = consistency_mask - min_sub_count
    consistency_mask = np.where(consistency_mask >= 0, 1, 0)

    # go into each subject and edit their weights.txt
    for subject in subjects:
        # source zip name
        subject_file_name = ""
        # path to source zip
        subject_zip = ""
        output_zip = ""

        # different source zip name and path if PARC_NAME present
        if PARC_NAME == "":
            subject_file_name = subject + "_tvb_inputs.zip"
            subject_zip = os.path.join(zip_dir, subject_file_name)
            output_zip = os.path.join(outputdir, subject_file_name)
        else:
            subject_file_name = subject + "_" + PARC_NAME + "_tvb_inputs.zip"
            subject_zip = os.path.join(zip_dir, subject_file_name)
            output_zip = os.path.join(outputdir, subject_file_name)

        if os.path.exists(subject_zip):
            # if specific dir exists then skip unzipping
            end_dir = os.path.join(outputdir, subject_file_name[:-4])
            SC_path = os.path.join(end_dir, "structural_inputs", "weights.txt")

            # load SCs again and apply consistency mask
            SC = ""
            if os.path.exists(SC_path):
                SC = np.loadtxt(SC_path)
                sc_has_nans = np.any(np.isnan(SC))
                if not sc_has_nans:
                    # threshold SC and save
                    SC = consistency_mask * SC
                    np.savetxt(SC_path, SC)

                    # load TL, remove ROIS, threshold, and save
                    TL_path = os.path.join(
                        end_dir, "structural_inputs", "tract_lengths.txt"
                    )
                    if os.path.exists(TL_path):
                        TL = np.loadtxt(TL_path)
                        TL = np.delete(TL, ROIs_to_remove, axis=0)
                        TL = np.delete(TL, ROIs_to_remove, axis=1)
                        TL = consistency_mask * TL
                        np.savetxt(TL_path, TL)

                    # load rest of struct tvb_input files to have ROIs removed and saved
                    cent_path = os.path.join(
                        end_dir, "structural_inputs", "centres.txt"
                    )
                    cort_path = os.path.join(
                        end_dir, "structural_inputs", "cortical.txt"
                    )
                    hemi_path = os.path.join(
                        end_dir, "structural_inputs", "hemisphere.txt"
                    )

                    single_row_ROI_remove = [cent_path, cort_path, hemi_path]

                    for input_file in single_row_ROI_remove:
                        if os.path.exists(input_file):
                            loaded_input = np.genfromtxt(
                                input_file, delimiter="\n", dtype="str"
                            )
                            loaded_input = np.delete(loaded_input, ROIs_to_remove)
                            # np.savetxt(input_file, loaded_input)
                            np.savetxt(
                                input_file, loaded_input, delimiter="\n", fmt="%s"
                            )
                    # load fc and ts files to remove ROIs
                    for file in os.listdir(os.path.join(end_dir, "functional_inputs")):
                        if file.endswith(".ica"):
                            FC_path = os.path.join(
                                end_dir,
                                "functional_inputs",
                                file,
                                file + "_functional_connectivity.txt",
                            )
                            TS_path = os.path.join(
                                end_dir,
                                "functional_inputs",
                                file,
                                file + "_time_series.txt",
                            )

                            if os.path.exists(FC_path):
                                FC = np.loadtxt(FC_path)
                                FC = np.delete(FC, ROIs_to_remove, axis=0)
                                FC = np.delete(FC, ROIs_to_remove, axis=1)
                                np.savetxt(FC_path, FC)

                            if os.path.exists(TS_path):

                                TS = np.loadtxt(TS_path)
                                TS = np.delete(TS, ROIs_to_remove, axis=1)
                                np.savetxt(TS_path, TS)

                    # zip and clean up
                    # if os.path.exists(os.path.join(end_dir,"structural_inputs")):
                    # removed if statement because implied by existenc of sc path

                    struct_zip = os.path.join(end_dir, "structural_inputs.zip")
                    # remove existing zip and save new for structural inputs
                    os.remove(struct_zip)
                    shutil.make_archive(
                        struct_zip[:-4], "zip", end_dir, "structural_inputs"
                    )

                    # remove uncompressed structural inputs dir
                    shutil.rmtree(os.path.join(end_dir, "structural_inputs"))

                    end_dir_thresh = end_dir + "_thresholded"  # _tvb_inputs
                    os.rename(end_dir, end_dir_thresh)

                    # make zip for this sub
                    shutil.make_archive(
                        end_dir_thresh,
                        "zip",
                        os.path.dirname(end_dir_thresh),
                        os.path.basename(end_dir_thresh),
                    )

                    shutil.rmtree(end_dir_thresh)
                else:
                    print("sub has nans - deleted", end_dir)
                    shutil.rmtree(end_dir)
            else:
                print("SC not found - deleted", end_dir)
                if os.path.exists(end_dir):
                    shutil.rmtree(end_dir)


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

    consistency_thresholding(
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
    )
