#!/bin/env python
#
# Script name: tvb_concat_probtrackx2.py
#
# Description: Script to generate dMRI/probtrackx data matrices.
#
## Author: Justin Wang

import numpy as np
import sys


def tvb_concat_probtrackx2(subj, PARC_NAME, batch=True):
    """Function that generates distance, fdt_network_matrix.txt,
    SC, waytotal, fdt_network_matrix for a subject.


    Parameters
    ----------
    subj :
        Full path to subject's directory.
    batch : bool, optional
        handles opening/concatenation of batched probtrackx files
        if True, opens in main dir if False
    """

    # calculating and saving SC, fdt_network_matrix, waytotal from all 10 batches
    m = 1
    fdt = ""
    way = ""

    # handles opening of batched outputs
    if batch:
        for m in range(1, 11):

            batch_dir = subj + "/dMRI/probtrackx_" + PARC_NAME + "/batch_" + str(m)

            if m == 1:
                fdt = np.loadtxt(batch_dir + "/fdt_network_matrix")
                way = np.loadtxt(batch_dir + "/waytotal")
            else:
                fdt = np.add(fdt, np.loadtxt(batch_dir + "/fdt_network_matrix"))
                way = np.add(way, np.loadtxt(batch_dir + "/waytotal"))

    else:

        standard_dir = subj + "/dMRI/probtrackx_" + PARC_NAME + ""

        fdt = np.loadtxt(standard_dir + "/fdt_network_matrix")
        way = np.loadtxt(standard_dir + "/waytotal")

    ones = np.ones(fdt.shape)
    way_matrix = np.multiply(way, ones)
    way_matrix = way_matrix.T

    SC = np.divide(fdt, way_matrix)

    # symmetrizing matrix
    SC = (SC + SC.T) / 2


    np.savetxt(subj + "/dMRI/probtrackx_" + PARC_NAME + "/fdt_network_matrix", fdt)
    np.savetxt(subj + "/dMRI/probtrackx_" + PARC_NAME + "/waytotal", way)
    np.savetxt(subj + "/dMRI/sc_" + PARC_NAME + ".txt", SC)

    # calculating and saving distance, fdt_network_matrix_lengths from all 10 batches
    if batch:
        m = 1
        mat_lengths = ""
        fdt1 = ""
        mtx = ""
        mat_sum = ""
        for m in range(1, 11):

            batch_dir = subj + "/dMRI/probtrackx_" + PARC_NAME + "/batch_" + str(m)

            if m == 1:
                mat_lengths = np.loadtxt(batch_dir + "/fdt_network_matrix_lengths")
                mat_lengths[np.isnan(mat_lengths)] = 0.0
                fdt1 = np.loadtxt(batch_dir + "/fdt_network_matrix")
                mtx = np.multiply(fdt1, mat_lengths)
                mat_sum = fdt1
            else:
                mat_lengths = np.loadtxt(batch_dir + "/fdt_network_matrix_lengths")
                mat_lengths[np.isnan(mat_lengths)] = 0.0
                fdt1 = np.loadtxt(batch_dir + "/fdt_network_matrix")
                mtx = np.add(mtx, np.multiply(fdt1, mat_lengths))
                mat_sum = np.add(mat_sum, fdt1)

        mat_sum_plus_transpose = mat_sum + mat_sum.T 
        tract_lengths_weighted = np.divide(mtx, mat_sum_plus_transpose)
        tract_lengths_weighted[np.isnan(tract_lengths_weighted)] = 0.0

        # symmetrizing matrix
        tract_lengths = tract_lengths_weighted + tract_lengths_weighted.T
        np.savetxt(subj + "/dMRI/distance_"+PARC_NAME+".txt", tract_lengths)
    else:
        standard_dir = subj + "/dMRI/probtrackx_"+PARC_NAME+""

        mat_lengths = np.loadtxt(standard_dir + "/fdt_network_matrix_lengths")
        fdt1 = np.loadtxt(standard_dir + "/fdt_network_matrix")
        fdt1_plus_transpose = fdt1 + fdt1.T 
        tract_lengths = mat_lengths
        tract_lengths[np.isnan(tract_lengths)] = 0.0
        tract_lengths_weighted = np.divide(np.multiply(tract_lengths,fdt1),fdt1_plus_transpose)
        tract_lengths_weighted[np.isnan(tract_lengths_weighted)] = 0.0

        # symmetrizing matrix
        tract_lengths = tract_lengths_weighted + tract_lengths_weighted.T
        np.savetxt(subj + "/dMRI/distance_"+PARC_NAME+".txt", tract_lengths)



if __name__ == "__main__":
    """Function that generates distance, fdt_network_matrix.txt,
    SC, waytotal, fdt_network_matrix for a subject.


    Usage
    ----------
    python  tvb_concat_probtrackx2.py  subj


    Arguments
    ----------
    subj :
        Full path to subject's directory.

    """
    # try:
    if len(sys.argv) > 2 and (sys.argv[3] == "gpu_batch" or sys.argv[3] == "false"):
        tvb_concat_probtrackx2(sys.argv[1], sys.argv[2], batch=True)
    else:
        tvb_concat_probtrackx2(sys.argv[1], sys.argv[2], batch=False)
