#!/bin/env python
# Script name: merge_bvecbval.py
#
# Description: Concatenates bval and bvec values into their respective merged files.
#
# Usage: python merge_bvecbval.py bval_file_1 bval_file_2 bvec_file_1 bvec_file_2 bval_output_file bvec_output_file
#
# Author: Leanne Rokos

import numpy as np
import sys


def merge_bvalbvec(
    bval_file_1,
    bval_file_2,
    bvec_file_1,
    bvec_file_2,
    bval_output_name,
    bvec_output_name,
):
    bval1 = np.loadtxt(bval_file_1)
    bval2 = np.loadtxt(bval_file_2)

    bvec1 = np.loadtxt(bvec_file_1)
    bvec2 = np.loadtxt(bvec_file_2)

    bval = np.concatenate((bval1, bval2))
    bval = bval[:, np.newaxis]
    bval = bval.T
    np.savetxt(bval_output_name, bval, fmt="%i")

    bvec = np.concatenate((bvec1, bvec2), axis=1)
    np.savetxt(bvec_output_name, bvec, fmt="%0.6f")


if __name__ == "__main__":
    """Function that concatenates bval and bvec values into their respective merged files.


    Usage
    ----------
    python merge_bvecbval.py bval_file_1 bval_file_2 bvec_file_1 bvec_file_2 bval_output_file bvec_output_file

    Arguments
    ----------
    bval_file_1
    bval_file_2
    bvec_file_1
    bvec_file_2
    bval_output_name
    bvec_output_name
    """

    merge_bvalbvec(
        sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
    )
