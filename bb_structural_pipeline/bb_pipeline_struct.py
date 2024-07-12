#!/bin/env python
#
# Script name: bb_pipeline_struct.py
#
# Description: Script with the structural pipeline.
# 			   This script will call the rest of structural functions.
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
import os
import numpy as np
import sys
import json

import bb_pipeline_tools.bb_logging_tool as lt
import logging

sys.path.insert(1, os.path.dirname(__file__) + "/..")


def bb_pipeline_struct(subject, run_top_up, file_configuration):
    logger = logging.getLogger()
    job_swi = "-1"
    job_struct_init = "-1"

    subject_name = subject.replace("/", "_")

    if ("T1" not in file_configuration) or (file_configuration["T1"] == ""):
        logger.error("There is no T1. Subject " + subject + " cannot be processed.")
        return -1

    else:
        # TODO: Adapt code to good syntax practices --> PEP 8

        # Create the B0 AP - PA file to estimate the fieldmaps
        b0_threshold = int(
            np.loadtxt(os.environ["BB_BIN_DIR"] + "/bb_data/b0_threshold.txt")
        )

        jobs_b0 = []

        if run_top_up:
            # if encDir in ["dwi"]:
            # pass
            logger.info("Running topup setup...")
            for encDir in ["AP", "PA"]:
                b_vals = np.loadtxt(subject + "/dMRI/raw/" + encDir + ".bval")
                num_vols = int(sum(b_vals <= b0_threshold))

                lt.run_command(
                    logger,
                    "$BB_BIN_DIR/bb_structural_pipeline/bb_get_b0s.py -i "
                    + subject
                    + "/dMRI/raw/"
                    + encDir
                    + ".nii.gz -o "
                    + subject
                    + "/fieldmap/total_B0_"
                    + encDir
                    + ".nii.gz -n "
                    + str(num_vols)
                    + " -l "
                    + str(b0_threshold),
                    "bb_get_b0s_1_" + subject_name,
                )

                jobs_b0.append(
                    lt.run_command(
                        logger,
                        "$BB_BIN_DIR/bb_structural_pipeline/bb_choose_bestB0 "
                        + subject
                        + "/fieldmap/total_B0_"
                        + encDir
                        + ".nii.gz "
                        + subject
                        + "/fieldmap/B0_"
                        + encDir
                        + ".nii.gz ",
                        "bb_choose_bestB0_1_" + subject_name,
                    )
                )

            lt.run_command(
                logger,
                "${FSLDIR}/bin/fslmerge -t "
                + subject
                + "/fieldmap/B0_AP_PA "
                + subject
                + "/fieldmap/B0_AP "
                + subject
                + "/fieldmap/B0_PA",
                "bb_fslmerge_" + subject_name,
            )
            logger.info("Top up setup COMPLETE.")

        # Registrations - T1 to MNI - T2 to T1 - T2 to MNI (Combining the 2 previous ones)
        logger.info("Running bb_struct_init...")
        job_struct_init = lt.run_command(
            logger,
            "${BB_BIN_DIR}/bb_structural_pipeline/bb_struct_init " + subject,
            "bb_struct_init_" + subject_name,
        )
        logger.info("bb_struct_init COMPLETE.")

        # TODO: Do a better check here. This one looks arbitrary
        if "SWI_TOTAL_MAG_TE2" in file_configuration:
            print("Running SWI registration...")
            job_swi = lt.run_command(
                logger,
                "$BB_BIN_DIR/bb_structural_pipeline/bb_swi_reg " + subject,
                "bb_swi_reg_" + subject_name,
            )
            logger.info("SWI registration COMPLETE.")

        # Top up
        if run_top_up:
            logger.info("Topup enabled. Running topup...")
            lt.run_command(
                logger,
                "$BB_BIN_DIR/bb_structural_pipeline/bb_prepare_struct_fieldmap "
                + subject,
                "bb_prepare_struct_fieldmap_" + subject_name,
            )

            lt.run_command(
                logger,
                "${FSLDIR}/bin/topup --imain="
                + subject
                + "/fieldmap/B0_AP_PA --datain="
                + subject
                + "/fieldmap/acqparams.txt --config=b02b0.cnf --out="
                + subject
                + "/fieldmap/fieldmap_out --fout="
                + subject
                + "/fieldmap/fieldmap_fout --jacout="
                + subject
                + "/fieldmap/fieldmap_jacout -v",
                "bb_topup_" + subject_name,
            )
            logger.info("Topup COMPLETE.")
        else:
            logger.error(
                "There is not enough/correct DWI data. TOPUP cannot be run. Continuing to run DWI and fMRI processing without TOPUP."
            )

        if not run_top_up:
            return ",".join([job_struct_init, job_swi])
        else:
            logger.info("Running post-topup...")
            job_post_top_up = lt.run_command(
                logger,
                "$BB_BIN_DIR/bb_structural_pipeline/bb_post_topup " + subject,
                "bb_post_topup_" + subject_name,
            )

            logger.info("Post-topup COMPLETE.")
            logger.info("Logfiles located in subject's logs directory.")
            return job_post_top_up


if __name__ == "__main__":
    # grab subject name from command
    subject_ = sys.argv[1]
    fd_fileName = "logs/file_descriptor.json"

    # check if subject directory exists
    json_path_name = f"./{subject_}/{fd_fileName}"
    if not os.path.isdir(subject_):
        print(f"{subject_} is not a valid directory. Exiting")
        sys.exit(1)
    # attempt to open the JSON file
    try:
        json_path = os.path.abspath(json_path_name)
        with open(json_path_name, "r") as f:
            fileConfig = json.load(f)
    except Exception:
        print(f"{json_path_name} could not be loaded. Exiting")
        sys.exit(1)
    # call pipeline
    bb_pipeline_struct(subject_, False, fileConfig)
