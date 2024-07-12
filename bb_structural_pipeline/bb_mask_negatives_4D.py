#!/bin/env python
#
# Script name: bb_mask_negatives_4D.py
#
# Description: Script to remove the negative values from a 4D image
#
# Authors: Fidel Alfaro-Almagro, Stephen M. Smith & Mark Jenkinson
#
# Copyright 2017 University of Oxford
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys, argparse, os.path
import nibabel as nib
import numpy as np
import os


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main():
    parser = MyParser(
        description="Creates a mask with the number of voxels across the 4D image that have either (0 or negative values) or (NaN)"
    )
    parser.add_argument("-i", dest="input", type=str, nargs=1, help="Input image file")
    parser.add_argument(
        "-o", dest="output", type=str, nargs=1, help="Output image file"
    )
    parser.add_argument(
        "-n",
        dest="checkNaNs",
        type=bool,
        default=False,
        nargs=1,
        help="Check NaNs instead of 0 or negative",
    )
    parser.add_argument(
        "-z",
        dest="checkZeros",
        type=bool,
        default=False,
        nargs=1,
        help="Check Zeros instead of 0 or negative",
    )

    argsa = parser.parse_args()

    if argsa.input == None:
        parser.print_help()
        exit()

    if argsa.output == None:
        parser.print_help()
        exit()

    np.set_printoptions(suppress=True)

    img1 = nib.load(argsa.input[0])

    data = img1.get_data()
    dims = data.shape

    numDims = len(dims)

    #    if dims.length ==3:

    if numDims == 4:
        numVolumes = dims[3]
    else:
        numVolumes = 1

    finalIm = np.zeros(dims[0:3])

    for i in range(0, numVolumes):
        if numVolumes == 1:
            im = data
        else:
            im = data[:, :, :, i]

        if argsa.checkZeros:
            x, y, z = np.where(im == 0)
        elif argsa.checkNaNs:
            x, y, z = np.where(np.isnan(im))
        else:
            x, y, z = np.where(im <= 0)
        for j in range(0, x.size):
            finalIm[x[j], y[j], z[j]] = finalIm[x[j], y[j], z[j]] + 1

    out = nib.Nifti1Image(finalIm, affine=img1.get_affine(), header=img1.get_header())

    nib.save(out, argsa.output[0])


if __name__ == "__main__":
    main()
