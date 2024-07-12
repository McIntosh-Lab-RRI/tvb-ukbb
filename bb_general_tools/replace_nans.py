#!/bin/env python
#

import sys
import numpy as np


def replace_nans(matrix_file):
    mat = np.loadtxt(matrix_file)
    mat = np.nan_to_num(mat, nan=0.0, neginf=0.0)
    np.savetxt(matrix_file, mat)


if __name__ == "__main__":
    """Function that generates replaces nans and neginfs in a file with zeroes.


    Usage
    ----------
    python  replace_nans.py  file_path


    Arguments
    ----------
    file_path :
        Full path to file in which nans should be replaced.

    """
    # try:
    replace_nans(sys.argv[1])
