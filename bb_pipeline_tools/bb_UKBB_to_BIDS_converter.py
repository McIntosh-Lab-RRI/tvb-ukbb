#!/bin/env python
#
# Script name: bb_UKBB_to_BIDS_converter.py
#
# Description: Script to convert a dataset with Biobank structure into BIDS.
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

import os
import re
import glob
import json
import copy
import nibabel as nib
import bb_logging_tool as LT
import sys, argparse, os.path, shutil

# import bb_general_tools.bb_path as bb_path
from subprocess import check_output

logger = None


def create_directories(subject):
    bidDirsFile = os.environ["BB_BIN_DIR"] + "/bb_data/BIDS_directories.json"
    with open(bidDirsFile, "r") as f:
        directories = json.load(f)

    for directory in directories:
        directory = directory.replace("@SUBJECT@", subject)
        if not os.path.isdir(directory):
            logger.info("Creating directory " + directory)
            os.makedirs(directory)
        else:
            logger.info("Directory " + directory + " already existed")


def create_links(subject):
    BB_to_BIDS_table_file = os.environ["BB_BIN_DIR"] + "/bb_data/UKBB_to_BIDS.json"
    with open(BB_to_BIDS_table_file, "r") as f:
        BB_to_BIDS_table = json.load(f)

    for BB_to_BIDS_key in BB_to_BIDS_table.keys():
        if os.path.isfile(BB_to_BIDS_key):
            newName = BB_to_BIDS_table[BB_to_BIDS_key].replace("@SUBJECT@", subject)

            # If the file is a nii.gz, create the link for it and the json file
            if BB_to_BIDS_key.endswith(".nii.gz"):
                os.symlink("../../../" + BB_to_BIDS_key, newName)
                logger.info(
                    "Created the symlink "
                    + newName
                    + " pointing to ../../../"
                    + BB_to_BIDS_key
                )

                if os.path.isfile(BB_to_BIDS_key.replace(".nii.gz", ".json")):
                    os.symlink(
                        "../../../" + BB_to_BIDS_key.replace(".nii.gz", "") + ".json",
                        newName.replace(".nii.gz", ".json"),
                    )
                    logger.info(
                        "Created the symlink "
                        + newName.replace(".nii.gz", ".json")
                        + " pointing to ../../../"
                        + BB_to_BIDS_key.replace(".nii.gz", ".json")
                    )
                else:
                    logger.info(
                        "There was a problem. Expected JSON file "
                        + BB_to_BIDS_key.replace(".nii.gz", "")
                        + ".json does not exist."
                    )

                # Including the TASK field in the task json files in bold files
                if newName.endswith("_bold.nii.gz"):
                    if os.path.isfile(newName.replace(".nii.gz", ".json")):
                        logger.info(
                            "Correcting the JSON file for "
                            + BB_to_BIDS_key.replace(".nii.gz", "")
                            + " to add the TaskName field, required in BIDS."
                        )
                        with open(newName.replace(".nii.gz", ".json"), "r") as fd:
                            jsonBold = json.load(fd)

                        fileNameSections = (newName.replace(".nii.gz", "")).split("_")
                        taskNameSection = [x for x in fileNameSections if "task" in x][
                            0
                        ]
                        taskName = taskNameSection.split("-")[1]

                        jsonBold["TaskName"] = taskName

                        os.remove(newName.replace(".nii.gz", ".json"))
                        fd = open(newName.replace(".nii.gz", ".json"), "w")
                        json.dump(
                            jsonBold,
                            fd,
                            sort_keys=True,
                            indent=4,
                            separators=(",", ": "),
                        )

                    # Including the events tsv file associated with the task fMRI
                    if not "rest" in newName:
                        origFile = (
                            os.environ["BB_BIN_DIR"] + "/bb_data/task-hariri_events.tsv"
                        )
                        newFile = (
                            os.environ["PWD"]
                            + "/"
                            + subject
                            + "/"
                            + newName.replace("_bold.nii.gz", "_events.tsv")
                        )
                        shutil.copyfile(origFile, newFile)

            # If the file is NOT a nii.gz, create the corresponding link
            else:
                os.symlink("../../../" + BB_to_BIDS_key, newName)
                logger.info(
                    "Created the symlink "
                    + newName
                    + " pointing to ../../../"
                    + BB_to_BIDS_key
                )

        else:
            logger.info(
                "Subject "
                + subject
                + " does not have the file "
                + BB_to_BIDS_key
                + " so no link was created."
            )


def bb_UKBB_to_BIDS_converter(subject):
    logger.info("Change dir to " + subject)
    os.chdir(subject)
    create_directories(subject)
    create_links(subject)
    logger.info("BIDS conversion for subject " + subject + " is finished.")


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main():
    global logger

    parser = MyParser(description="BioBank Pipeline FILE Manager")
    parser.add_argument("subjectFolder", help="Subject Folder")

    argsa = parser.parse_args()

    subject = argsa.subjectFolder
    subject = subject.strip()

    if subject[-1] == "/":
        subject = subject[0 : len(subject) - 1]

    logger = LT.init_logging(__file__, subject)

    logger.info("Running UK Biobank to BIDS converter")
    bb_UKBB_to_BIDS_converter(subject)

    LT.finish_logging(logger)


if __name__ == "__main__":
    main()
