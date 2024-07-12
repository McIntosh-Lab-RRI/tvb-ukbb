#!/bin/env python
#
# Script name: bb_get_phase.py
#
# Description: Script to get the phase of a subject, based on the acq date.
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

import glob
import json
import sys, argparse, os.path
from bb_read_json_field import bb_read_json_field


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main():
    parser = MyParser(description="BioBank Phase Reader")
    parser.add_argument("subjectFolder", help="Subject Folder")

    argsa = parser.parse_args()

    subject = argsa.subjectFolder
    subject = subject.strip()

    fileDir = subject + "/T1"

    fileName = fileDir + "/T1.json"

    if not os.path.isfile(fileName):
        foundFile = glob.glob(fileDir + "/*/T1.json")
        if foundFile == []:
            print("-1")
            exit(1)
        else:
            fileName = foundFile[0]

    res = bb_read_json_field(fileName, "AcquisitionDateTime")

    if res == []:
        print("-1")
        exit(1)
    else:
        res = float(res)

    with open(os.environ["BB_BIN_DIR"] + "/bb_data/phases_dates.json") as data_file:
        phases_dates = json.load(data_file)

    for key in phases_dates.keys():
        if (phases_dates[key][0] <= res) and (res <= phases_dates[key][1]):
            print(key)
            exit(0)

    print("-1")


if __name__ == "__main__":
    main()
