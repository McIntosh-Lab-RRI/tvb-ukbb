#!/bin/env python

import nibabel as nib
import numpy as np
import sys
import csv
import os


np.set_printoptions(threshold=sys.maxsize)


def generate_centres_cortical(subjdir, PARC_LUT, PARC_NAME):
    datafile = open(PARC_LUT, "r")
    datareader = csv.reader(datafile, delimiter="\t")
    ROI_list = []

    for row in datareader:
        row[0] = int(row[0])
        ROI_list.append(row)

    # ROI_list=sorted(ROI_list,key=lambda l:l[0])

    label_image = os.path.join(subjdir, "T1/labelled_GM_" + PARC_NAME + ".nii.gz")
    img = nib.load(label_image)
    data = img.get_fdata()
    # print(t1_data[np.nonzero(t1_data)])

    centres_file = os.path.join(subjdir, "tvb_inputs/structural_inputs/centres.txt")
    cortical_file = os.path.join(subjdir, "tvb_inputs/structural_inputs/cortical.txt")
    hemi_file = os.path.join(subjdir, "tvb_inputs/structural_inputs/hemisphere.txt")

    f = open(centres_file, "a")
    g = open(cortical_file, "a")
    h = open(hemi_file, "a")
    for row in ROI_list:
        ROI_num = row[0]
        ROI_name = row[1]
        result = np.where(data == ROI_num)
        x_cog = (np.mean(result[0]) - (img.header["dim"][1] - 1) / 2) * img.header[
            "pixdim"
        ][1]
        y_cog = (np.mean(result[1]) - (img.header["dim"][2] - 1) / 2) * img.header[
            "pixdim"
        ][2]
        z_cog = (np.mean(result[2]) - (img.header["dim"][3] - 1) / 2) * img.header[
            "pixdim"
        ][3]

        # some of the ROIs in LUT arent in the SCFC... how do we know which ones will be used for the final weights matrices?
        if np.isnan(x_cog) or np.isnan(y_cog) or np.isnan(z_cog):
            print("found nan")

        f.write(
            str(row[1])
            + "\t"
            + str(x_cog)
            + "\t"
            + str(y_cog)
            + "\t"
            + str(z_cog)
            + "\n"
        )

        # todo find pattern for subcort/cort
        # if ROI_num > 400:
        if "lh" in ROI_name or "rh" in ROI_name:
            g.write("0\n")
        else:
            g.write("1\n")

        if "lh" in ROI_name or "LH" in ROI_name:
            h.write("0\n")
        else:
            h.write("1\n")

    f.close()
    g.close()
    h.close()


if __name__ == "__main__":
    """Function that generates SC, FC, TL, TS plots for QC html report
    for a subject.


    Usage
    ----------
    python  SC_FC.py  subj


    Arguments
    ----------
    subj :
        Full path to subject's directory.

    """
    # try:

    generate_centres_cortical(sys.argv[1], sys.argv[2], sys.argv[3])
