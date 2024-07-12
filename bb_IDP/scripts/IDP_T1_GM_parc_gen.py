#!/bin/env python
#
# Script name: IDP_T1_GM_parc_gen.py
#
# Description: Script to generate the bb_IDP_T1_GM_parcellation IDP file.
#
## Author: Justin Wang
import nibabel as nib
import numpy as np
import sys
import os


def IDP_T1_GM_parc_gen(PARC_LUT, IDP_file, parcel_to_T1, pve_1):
    parcel_img = nib.load(
        parcel_to_T1
    )  # "/Users/justinwang/Documents/McIntosh/sub-003S6264/T1/transforms/parcel_to_T1.nii.gz"
    GM_img = nib.load(
        pve_1
    )  # "/Users/justinwang/Documents/McIntosh/sub-003S6264/T1/T1_fast/T1_brain_pve_1.nii.gz"

    parcel_data = parcel_img.get_fdata()
    GM_data = GM_img.get_fdata()

    result = ""

    lines = ""
    with open(PARC_LUT) as f:
        lines = f.read().splitlines()

    ROI_num_list = []
    for line in lines:
        ROI_num_list.append(int(line.split("\t")[0]))

    for x in ROI_num_list:
        num_voxels_in_ROI = np.count_nonzero(parcel_data == x)

        bb_IDP_T1_GM_parcellation = "NaN"

        if num_voxels_in_ROI != 0:
            ROI_voxels = np.where(parcel_data == x)
            mean_intensity_in_ROI = np.mean(GM_data[ROI_voxels])

            bb_IDP_T1_GM_parcellation = num_voxels_in_ROI * mean_intensity_in_ROI

        if result == "":
            result = str(bb_IDP_T1_GM_parcellation)
        else:
            result = result + " " + str(bb_IDP_T1_GM_parcellation)

    result = result + "\n"
    f = open(IDP_file, "w")
    f.write(result)
    f.close()


if __name__ == "__main__":
    """Function that reorganizes pve files that have been mislabelled.


    Usage
    ----------
    python  rename_pve.py  brain pve0 pve1 pve2


    Arguments
    ----------
    PARC_LUT: full file path to PARC_LUT

    IDP_file: full file path to bb_IDP_T1_GM_parcellation.txt

    parcel_to_T1: full file path to parcel_to_T1 file

    pve_1: full file path to pve_1


    """
    # try:
    IDP_T1_GM_parc_gen(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
