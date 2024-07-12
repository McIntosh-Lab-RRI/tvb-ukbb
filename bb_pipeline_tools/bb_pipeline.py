#!/bin/env python
#
# Script name: bb_pipeline.py
#
# Description: Main script. This script will call the rest of scripts.
#
# Authors: Fidel Alfaro-Almagro, Stephen M. Smith & Mark Jenkinson

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

import os
import sys
import argparse
import os.path
import logging
import shutil
import bb_logging_tool as logging_tool

from bb_file_manager import bb_file_manager
from bb_basic_QC import bb_basic_qc
from tvb_reparcellate_pipeline import tvb_reparcellate_pipeline
from bb_structural_pipeline.bb_pipeline_struct import bb_pipeline_struct
from bb_functional_pipeline.bb_pipeline_func import bb_pipeline_func
from bb_diffusion_pipeline.bb_pipeline_diff import bb_pipeline_diff
from bb_IDP.bb_IDP import bb_idp
from tvb_bb_QC.tvb_bb_QC import tvb_bb_qc


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


def main(cli_args=None):
    # INPUT VALIDATION
    if cli_args is None:
        parser = MyParser(description="BioBank Pipeline Manager")
        parser.add_argument("subjectFolder", help="Subject Folder")

        args = parser.parse_args()
    else:
        parser = MyParser(description="BioBank Pipeline Manager")
        parser.add_argument("subjectFolder", help="Subject Folder")
        args = parser.parse_args(cli_args)

    # SUBJECT PROCESSING
    subject = args.subjectFolder
    subject = subject.strip()

    if subject[-1] == "/":
        subject = subject[0 : len(subject) - 1]


    # LOGGING INITIALIZATION
    logger = logging.getLogger()
    logger.info("Configuring logger...")
    logger = logging_tool.init_logging(subject)
    logger.info("Logger configured.")

    # WORKFLOW HANDLING
    reparcellate = os.environ["REPARCELLATE"]
    parc_name = os.environ["PARC_NAME"]

    if reparcellate == "true":
        # REPARCELLATION PIPELINE
        # reparcellation
        logger.info("RUNNING reparcellation...")
        tvb_reparcellate_pipeline(subject, "none", parc_name)
        logger.info("Reparcellation COMPLETE.")

        # clean up
        logger.info("Main reparcellation pipeline COMPLETE.")

    if reparcellate == "false":
        logger.info("Cleaning directory and removing old files...")
        # Remove old intermediate data from previous runs
        retain = ["rawdata"]

        # loop through all files/folders in subject directory
        os.chdir(subject)
        for item in os.listdir(os.getcwd()):
            # if file/folder not in retain list, remove
            if item not in retain:
                if os.path.isdir(item):
                    shutil.rmtree(item)
                else:
                    os.remove(item)

        logger.info("Cleaning complete.")

        os.chdir("..")

        # PIPELINE
        # file manager
        logger.info("RUNNING file manager...")
        file_config = bb_file_manager(subject)
        logger.info("bb_file_manager COMPLETE.")

        logger.info("File configuration before QC:\n\t" + str(file_config))
        file_config = bb_basic_qc(subject, file_config)
        logger.info(
            "File configuration after running file manager:\n\t" + str(file_config)
        )

        # run_top_up ==> Having field-map
        if not (
            (("AP" in file_config) and (file_config["AP"] != ""))
            and (("PA" in file_config) and (file_config["PA"] != ""))
        ):
            logger.warning(
                "There is no proper AP/PA data. Thus, TOP UP will not be run"
            )
            run_top_up = False
            logger.warning("NO TOP UP")
        else:
            run_top_up = True

        # structural pipeline
        logger.info("RUNNING structural pipeline...")
        bb_pipeline_struct(subject, run_top_up, file_config)
        logger.info("Structural pipeline COMPLETE.")

        # functional pipeline
        logger.info("RUNNING Functional pipeline...")
        bb_pipeline_func(subject, file_config)
        logger.info("Functional pipeline COMPLETE.")

        # diffusion pipeline
        logger.info("RUNNING diffusion pipeline...6")
        bb_pipeline_diff(subject)
        logger.info("Diffusion pipeline COMPLETE.")

        # image dependent phenotype
        logger.info("RUNNING IDP...")
        bb_idp(subject)
        logger.info("IDP COMPLETE")

        # quality control
        logger.info("RUNNING QC pipeline...")
        tvb_bb_qc(subject)
        logger.info("QC pipeline COMPLETE.")

        # clean up
        logger.info("Main pipeline COMPLETE.")

    else:
        logger.error(
            'Invalid reparcellation argument\n Check environment variable "REPARCELLATE"'
        )


if __name__ == "__main__":
    main()
