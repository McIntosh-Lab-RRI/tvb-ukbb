#!/bin/env python
#
# Script name: bb_get_b0s.py
#
# Description: Script to select a particular B0 from a 4D file.
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
from subprocess import check_output


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main():
    parser = MyParser(description="UK Biobank tool to get a B0 of a set of B0 images")
    parser.add_argument("-i", dest="inputFile", type=str, nargs=1, help="Input File")
    parser.add_argument("-o", dest="outputFile", type=str, nargs=1, help="Output File")
    parser.add_argument(
        "-n",
        dest="desiredNumber",
        type=int,
        default=[4],
        nargs=1,
        help="Desired number of B0s from file. (Default: 4)",
    )
    parser.add_argument(
        "-l",
        dest="B0limit",
        type=int,
        default=[100],
        nargs=1,
        help="Limit B0 value. (Default 50)",
    )
    parser.add_argument(
        "-a",
        dest="bvalFilename",
        type=str,
        default="",
        nargs=1,
        help="bval file. (Default: Same basename as the input file)",
    )

    argsa = parser.parse_args()

    if argsa.inputFile == None:
        parser.print_help()
        exit()

    if argsa.outputFile == None:
        parser.print_help()
        exit()

    baseDir = os.path.dirname(argsa.inputFile[0])
    outDir = os.path.dirname(argsa.outputFile[0])
    baseN = os.path.basename(argsa.inputFile[0]).split(".")[0]
    outN = os.path.basename(argsa.outputFile[0]).split(".")[0]

    if argsa.bvalFilename == "":
        bvalFilename = baseDir + "/" + baseN + ".bval"
    else:
        bvalFilename = argsa.bvalFilename[0]

    f = open(bvalFilename)

    line = f.readlines()

    line = line[0].split()

    B0_intesity_limit = int(argsa.B0limit[0])

    indices = [i for i, x in enumerate(line) if int(x) < B0_intesity_limit]

    if argsa.desiredNumber[0] > len(indices):
        print(
            (
                "There are only %i B0. It is not possible to have %i"
                % (len(indices), argsa.desiredNumber[0])
            )
        )
        exit()

    if argsa.desiredNumber[0] <= 0:
        print("The number of B0 must be positive")
        exit()

    f = open(outDir + "/" + outN + "_indices.txt", "w")
    f.write(" ".join([str(x) for x in indices]))
    f.close()

    indices = indices[0 : argsa.desiredNumber[0]]

    output = check_output(
        "$FSLDIR/bin/fslselectvols -i "
        + argsa.inputFile[0]
        + " -o "
        + argsa.outputFile[0]
        + " --vols="
        + ",".join(str(i) for i in indices),
        shell=True,
    )


if __name__ == "__main__":
    main()
