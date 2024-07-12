#!/bin/env python
#
# Script name: bb_correct_image_names.py
#
# Description:Script to deal with a problem in the DICOM to NIFTI conversion
# 			  that introduces superfluous leading 0s for some numbers.
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
import bb_general_tools.bb_path as bb_path


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def bb_correct_image_names(folder):
    possibleExtensions = [".nii", ".nii.gz", ".bval", ".bvec", ".json"]

    listFiles = glob.glob(folder + "/*.*")

    for fullFileName in listFiles:
        try:
            extension = bb_path.getExt(fullFileName, possibleExtensions)
            fileName = bb_path.removeExt(fullFileName, possibleExtensions)
        except ValueError:
            continue

        parts = fileName.split("_")

        for i, part in enumerate(parts):
            try:
                intPart = int(part)
                parts[i] = part.lstrip("0")

            except ValueError:
                pass

        newFullFileName = "_".join(parts) + extension
        if newFullFileName != fullFileName:
            print("Moving " + fullFileName + " to " + newFullFileName)
            os.rename(fullFileName, newFullFileName)


def main():
    parser = MyParser(
        description="BioBank Tool to correct a problem from files coming out of dcm2niix"
    )
    parser.add_argument("folder", help="Folder to process")

    argsa = parser.parse_args()

    folder = argsa.folder
    folder = folder.strip()

    bb_correct_image_names(folder)


if __name__ == "__main__":
    main()
