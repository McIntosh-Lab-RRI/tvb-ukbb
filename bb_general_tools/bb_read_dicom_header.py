#!/bin/env python
#
# Script name: bb_read_dicom_header.py
#
# Description: Script to read the header of a DICOM file and print it.
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
import re
import os
import glob
import time
import dicom
import logging
import sys, argparse, os.path


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main():
    parser = MyParser(description="BioBank Dicom Header Reader")
    parser.add_argument("-f", dest="file", type=str, nargs=1, help="Read dicom file")
    parser.add_argument("--all", dest="allFields", action="store_true")

    allFields = False

    argsa = parser.parse_args()

    if argsa.file == None:
        parser.print_help()
        exit()

    if argsa.allFields == True:
        allFields = True

    fileName = argsa.file[0]

    ds = dicom.read_file(fileName)

    if not allFields:
        excludedFilesListFileName = (
            os.environ["BB_BIN_DIR"] + "/bb_data/dicom_fields_to_exclude.txt"
        )

        with open(excludedFilesListFileName) as f:
            hexKeys = f.readlines()
        for hexKey in hexKeys:
            keys = [int(x, 0) for x in hexKey.split()]
            ds[keys].value = ""

    print(ds)


if __name__ == "__main__":
    main()
