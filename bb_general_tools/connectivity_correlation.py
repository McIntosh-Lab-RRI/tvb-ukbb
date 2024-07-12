#!/bin/env python

import numpy as np
import sys
from scipy.stats import zscore
import matplotlib.pyplot as plt

import matplotlib
import os
import copy
from scipy.stats.stats import pearsonr



def connectivity_correlation(first_matrix, second_matrix, load):
    if load == True or load == "True":
        # load and flatten
        first = np.loadtxt(first_matrix)
        second = np.loadtxt(second_matrix)
    else:
        first = first_matrix
        second = second_matrix

    first = np.triu(first)
    second = np.triu(second)

    first = first.flatten()
    second = second.flatten()

    # mask out nans
    bad = ~np.logical_or(np.isnan(first), np.isnan(second))
    first = np.compress(bad, first)  # array([  5.,   1.,   6.,  10.,   1.,   1.])
    second = np.compress(bad, second)  # array([ 4.,  4.,  5.,  6.,  1.,  8.])

    # mask out inf
    bad = ~np.logical_or(np.isinf(first), np.isinf(second))
    first = np.compress(bad, first)  # array([  5.,   1.,   6.,  10.,   1.,   1.])
    second = np.compress(bad, second)  # array([ 4.,  4.,  5.,  6.,  1.,  8.])

    print(str(pearsonr(second, first)))
    return pearsonr(second, first)


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

    connectivity_correlation(sys.argv[1], sys.argv[2], sys.argv[3])
