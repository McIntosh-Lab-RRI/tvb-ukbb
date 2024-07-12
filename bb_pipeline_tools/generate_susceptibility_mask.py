#!/bin/env python

import nibabel as nib
import numpy as np
import sys
import csv
import os

np.set_printoptions(threshold=sys.maxsize)


def generate_susceptiblity_mask(new_parc, orig_suscep, new_PARC_LUT, new_suscept_name):

    datafile = open(new_PARC_LUT, "r")
    datareader = csv.reader(datafile, delimiter="\t")
    ROI_list = []
    for row in datareader:
        row[0] = int(row[0])
        ROI_list.append(row)

    new_img = nib.load(new_parc)
    new_data = new_img.get_fdata()

    suscept_img = nib.load(orig_suscep)
    suscept_data = suscept_img.get_fdata()


    suscept_mask = np.where(suscept_data > 0, 1, 0)
    new_suscept = 0 * suscept_mask
    for row in ROI_list:
        ROI_num = row[0]
        roi_match = np.where(new_data == ROI_num, new_data, 0)

        percent_ROI_masked = np.count_nonzero(
            roi_match * suscept_data
        ) / np.count_nonzero(roi_match)
        if percent_ROI_masked >= 0.25:
            new_suscept = new_suscept + roi_match

    clipped_img = nib.Nifti1Image(new_suscept, new_img.affine, new_img.header)
    nib.save(clipped_img, os.path.join(os.path.dirname(orig_suscep), new_suscept_name))

    # find in new_img that matches roi_num
    #
    # find in mask how many match new_img match
    # if > 25% of num
    # create a sum where its a bunch of ROI_nums
    # add ROI_num mask to new mask


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
    generate_susceptiblity_mask(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
