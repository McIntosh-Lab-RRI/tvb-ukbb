#!/bin/env python
#
# Script name: bb_pipeline_func.py
#
# Description: Script with the functional pipeline.
# 			   This script will call the rest of functional functions.
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
import logging
import os.path
import sys
import json
import bb_pipeline_tools.bb_logging_tool as lt

sys.path.insert(1, os.path.dirname(__file__) + "/..")


def bb_pipeline_func(subject, file_configuration):
    logger = logging.getLogger()
    log_dir = logger.log_dir
    base_dir = logger.base_dir + "/" + subject

    jobs_to_wait_for = ""

    subject_name = subject.replace("/", "_")

    # st = (
    #     # '${FSLDIR}/bin/fsl_sub -T 5 -N "bb_postprocess_struct_'
    #     '${FSLDIR}/bin/fsl_sub -q ${QUEUE_STANDARD} -N "bb_postprocess_struct_'
    #     + subject_name
    #     + '" -l '
    #     + log_dir
    #     + " -j "
    #     + str(jobHold)
    #     + "$BB_BIN_DIR/bb_functional_pipeline/bb_postprocess_struct "
    #     + subject
    # )

    # print(st)

    logger.info("Beginning functional pipeline")

    logger.info("Running bb_postprocess_struct...")
    lt.run_command(
        logger,
        "$BB_BIN_DIR/bb_functional_pipeline/bb_postprocess_struct " + subject,
        "bb_postprocess_struct_" + subject_name,
    )
    logger.info("bb_postprocess_struct completed")

    if ("rfMRI" in file_configuration) and (file_configuration["rfMRI"] != ""):
        logger.info("rfMRI files found. Running rfMRI subpipe")

        logger.info("Running rfMRI prep...")
        lt.run_command(
            logger,
            "$BB_BIN_DIR/bb_functional_pipeline/bb_prepare_rfMRI " + subject,
            "bb_prepare_rfMRI_" + subject_name,
        )
        logger.info("rfMRI prep completed.")

        logger.info("Running FEAT...")
        lt.run_command(
            logger,
            "feat " + base_dir + "/fMRI/rfMRI.fsf " + subject,
            "bb_feat_rfMRI_ns_" + subject_name,
        )
        logger.info("FEAT completed.")

        logger.info("Running FIX...")
        lt.run_command(
            logger,
            "$BB_BIN_DIR/bb_functional_pipeline/bb_fix " + subject,
            "bb_fix_" + subject_name,
        )
        logger.info("FIX completed.")

        logger.info("Running FC...")

        # Functional connectivity
        logger.info("Running functional connectivity...")
        lt.run_command(
            logger,
            "$BB_BIN_DIR/bb_functional_pipeline/tvb_FC " + subject,
            "tvb_FC_" + subject_name,
        )
        logger.info("FC completed.")

        # don't generate group-ICA RSNs
        # jobDR = lt.runCommand(
        # logger,
        # '${FSLDIR}/bin/fsl_sub -T 120  -N "bb_ICA_dr_'
        # '${FSLDIR}/bin/fsl_sub -q ${QUEUE_MORE_MEM}  -N "bb_ICA_dr_'
        # + subject_name
        # + '"  -l '
        # + log_dir
        # + " -j "
        # + jobFIX
        # + "$BB_BIN_DIR/bb_functional_pipeline/bb_ICA_dual_regression "
        # + subject,
        # )
        logger.info("Cleaning up rfMRI files...")
        job_clean = lt.run_command(
            logger,
            "$BB_BIN_DIR/bb_functional_pipeline/bb_clean_fix_logs " + subject,
            "bb_rfMRI_clean_" + subject_name,
        )
        logger.info("Done.")

        logger.info("rfMRI subpipe complete.")

        jobs_to_wait_for = job_clean

    else:
        logger.error(
            "There is no rFMRI info. Thus, the Resting State part will not be run"
        )

    if ("tfMRI" in file_configuration) and (file_configuration["tfMRI"] != ""):
        logger.info("tfMRI files found. Running tfMRI subpipeline")

        logger.info("Running tfMRI prep...")
        lt.run_command(
            logger,
            "$BB_BIN_DIR/bb_functional_pipeline/bb_prepare_tfMRI " + subject,
            "bb_prepare_tfMRI_" + subject_name,
        )
        logger.info("tfMRI prep complete.")

        logger.info("Running FEAT...")
        job_feat_t = lt.run_command(
            logger,
            "feat  " + base_dir + "/fMRI/tfMRI.fsf",
            "bb_feat_tfMRI_" + subject_name,
        )
        logger.info("FEAT completed.")

        if jobs_to_wait_for != "":
            jobs_to_wait_for = jobs_to_wait_for + "," + job_feat_t
        else:
            jobs_to_wait_for = "" + job_feat_t

        logger.info("tfMRI subpipe complete.")

    else:
        logger.error(
            "There is no tFMRI info. Thus, the Task Functional part will not be run"
        )

    if jobs_to_wait_for == "":
        jobs_to_wait_for = "-1"

    logger.info("Functional pipeline complete.")

    return jobs_to_wait_for


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
    bb_pipeline_func(subject_, fileConfig)
