#!/bin/env python
#
# Script name: bb_basic_QC.py
#
# Description: Script to run a basic QC test checking the dims of the image.
#
# Authors: Fidel Alfaro-Almagro, Stephen M. Smith & Mark Jenkinson
#
# Contributors: Patrick Mahon (pmahon@sfu.ca)
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
import logging
import os
import glob
import json
import sys
import argparse
import os.path

idealConfig = {}
fileConfig = {}


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


def make_unusable(file_name, list_dependent_dirs):
    if file_name.startswith("rfMRI"):
        directory = "fMRI"
        os.chdir(directory)
        files_in_dir = glob.glob("./rfMRI*")

        if "unusable" not in files_in_dir:
            os.mkdir("unusable")
            for file_to_move in files_in_dir:
                os.rename(file_to_move, "unusable/" + file_to_move)
            f = open("info_rfMRI.txt", "a")
            f.write("4 0 Missing needed file/modality")
            f.close()

    elif file_name.startswith("tfMRI"):
        directory = "fMRI"
        os.chdir(directory)
        files_in_dir = glob.glob("./tfMRI*")

        if "unusable" not in files_in_dir:
            os.mkdir("unusable")
            for file_to_move in files_in_dir:
                os.rename(file_to_move, "unusable/" + file_to_move)
            f = open("info_tfMRI.txt", "a")
            f.write("4 0 Missing needed file/modality")
            f.close()

    else:
        for directory in list_dependent_dirs:
            os.chdir(directory)
            files_in_dir = glob.glob("./*")

            if "unusable" not in files_in_dir:
                os.mkdir("unusable")
                for file_to_move in files_in_dir:
                    os.rename(file_to_move, "unusable/" + file_to_move)

                f = open("info.txt", "w")

                if directory == "T1":
                    f.write("2 0 Missing T1")
                else:
                    f.write("4 0 Missing needed modality")
                f.close()

            os.chdir("..")


def bb_basic_qc(subject, file_config):
    keys_to_pop = []
    os.chdir(subject)

    fd_file_name = "logs/file_descriptor.json"

    for key_to_pop in keys_to_pop:
        file_config.pop(key_to_pop, None)

    fd = open(fd_file_name, "w")
    json.dump(file_config, fd, sort_keys=True, indent=4, separators=(",", ": "))
    fd.close()

    os.chdir("..")

    return file_config


def main():
    parser = MyParser(description="BioBank basic QC tool")
    parser.add_argument("subjectFolder", help="Subject Folder")

    args_a = parser.parse_args()
    subject = args_a.subjectFolder
    subject = subject.strip()

    if subject[-1] == "/":
        subject = subject[0 : len(subject) - 1]

    ideal_config_file = os.environ["BB_BIN_DIR"] + "/bb_data/ideal_config.json"
    with open(ideal_config_file, "r") as f:
        file_config = json.load(f)

    logger = logging.getLogger()
    logger.info("Running file manager")
    bb_basic_qc(subject, file_config)


if __name__ == "__main__":
    main()
