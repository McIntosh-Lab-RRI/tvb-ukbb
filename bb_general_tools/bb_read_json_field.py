#!/bin/env python
#
# Script name: bb_read_json_field.py
#
# Description: Script/functions to read a certain field from a json file.
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
import json
import numbers
import sys, argparse, os.path


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def bb_read_json_field(fileName, fieldName, rounding=0, multFactor=1):
    result = []
    with open(fileName) as data_file:
        data = json.load(data_file)

    if fieldName in data.keys():
        value = data[fieldName]
        if isinstance(value, numbers.Number):
            if rounding != 0:
                result = round(data[fieldName] * multFactor, rounding)
            else:
                result = data[fieldName] * multFactor
        else:
            result = str(data[fieldName])

    return result


def main():
    parser = MyParser(description="BioBank Dicom Header Reader")
    parser.add_argument("-F", dest="file", type=str, nargs=1, help="Read json file")
    parser.add_argument(
        "-f", dest="field", type=str, nargs=1, default="NONE", help="Read field"
    )
    parser.add_argument(
        "-r",
        dest="rounding",
        type=int,
        default=0,
        help="Round the value the selected number of decimals (Default: No rounding",
    )
    parser.add_argument(
        "-m",
        dest="multFactor",
        type=float,
        default=1,
        help="Multiplication factor for the selected value (Default 1)",
    )

    argsa = parser.parse_args()

    if argsa.file == None:
        parser.print_help()
        exit()

    if argsa.field == None:
        parser.print_help()
        exit()

    rounding = argsa.rounding
    multFactor = argsa.multFactor

    fileName = argsa.file[0]
    fieldName = argsa.field[0]

    res = bb_read_json_field(fileName, fieldName, rounding, multFactor)

    print(str(res))


if __name__ == "__main__":
    main()
