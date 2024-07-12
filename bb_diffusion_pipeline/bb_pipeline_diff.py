#!/bin/env python
#
# Script name: bb_pipeline_diff.py
#
# Description: Script with the dMRI pipeline.
# 			   This script will call the rest of dMRI functions.
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


def bb_pipeline_diff(subject):
    logger = logging.getLogger()

    log_dir = logger.log_dir
    base_dir = log_dir[0 : log_dir.rfind("/logs/")]

    subject_name = subject.replace("/", "_")

    logger.info("Beginning diffusion pipeline")

    logger.info("Running pre_eddy...")
    lt.run_command(
        logger,
        "$BB_BIN_DIR/bb_diffusion_pipeline/bb_eddy/bb_pre_eddy " + subject,
        "bb_pre_eddy_" + subject_name,
    )
    logger.info("pre_eddy completed.")

    if os.environ["SynB0"] == "y":
        logger.info("Running SynB0 unwarping...")
        lt.run_command(
            logger,
            "$BB_BIN_DIR/bb_diffusion_pipeline/tvb_SynB0/tvb_SynB0_pipeline.sh "
            + subject,
            "tvb_bb_SynB0_pipeline_" + subject_name,
        )
        logger.info("SynB0 unwarping done.")

    logger.info("Running eddy..")
    lt.run_command(
        logger,
        "$BB_BIN_DIR/bb_diffusion_pipeline/bb_eddy/bb_eddy_wrap " + base_dir,
        "bb_eddy_" + subject_name,
    )
    logger.info("eddy completed.")

    logger.info("Running post_eddy...")
    lt.run_command(
        logger,
        "$BB_BIN_DIR/bb_diffusion_pipeline/bb_eddy/bb_post_eddy " + base_dir,
        "bb_post_eddy_" + subject_name,
    )

    logger.info("post_eddy completed.")

    logger.info("Running DTIFIT...")
    lt.run_command(
        logger,
        "${FSLDIR}/bin/dtifit -k "
        + base_dir
        + "/dMRI/dMRI/data_1_shell -m "
        + base_dir
        + "/dMRI/dMRI/nodif_brain_mask -r "
        + base_dir
        + "/dMRI/dMRI/data_1_shell.bvec -b "
        + base_dir
        + "/dMRI/dMRI/data_1_shell.bval -o "
        + base_dir
        + "/dMRI/dMRI/dti",
        "bb_dtifit_" + subject_name,
    )
    logger.info("DTIFIT completed.")

    logger.info("Running TBSS...")
    lt.run_command(
        logger,
        "$BB_BIN_DIR/bb_diffusion_pipeline/bb_tbss/bb_tbss_general " + subject,
        "bb_tbss_" + subject_name,
    )
    logger.info("TBSS completed.")
    # jobNODDI = lt.runCommand(
    # logger,
    # '${FSLDIR}/bin/fsl_sub -T 100 -N "bb_NODDI_'
    # '${FSLDIR}/bin/fsl_sub -q ${QUEUE_MORE_MEM} -N "bb_NODDI_'
    # + subject_name
    # + '" -j '
    # + jobTBSS
    # + "  -l "
    # + log_dir
    # + "$BB_BIN_DIR/bb_diffusion_pipeline/bb_NODDI "
    # + subject,
    # )

    logger.info("Running pre_bedpostx...")
    lt.run_command(
        logger,
        "$BB_BIN_DIR/bb_diffusion_pipeline/bb_bedpostx/bb_pre_bedpostx_gpu "
        + base_dir
        + "/dMRI",
        "bb_pre_bedpostx_gpu_" + subject_name,
    )
    logger.info("pre_bedpostx completed.")

    logger.info("Running bedpostx...")
    lt.run_command(
        logger,
        "$BB_BIN_DIR/bb_diffusion_pipeline/bb_bedpostx/bb_bedpostx_gpu "
        + base_dir
        + "/dMRI",
        "bb_bedpostx_gpu_" + subject_name,
    )
    logger.info("bedpostx completed.")

    # bb_post_bedpostx_gpu not necessary if using bedpostx package rather than xfibres (gpu) #####
    # lt.runCommand(
    # logger,
    # '${FSLDIR}/bin/fsl_sub -T 15  -N "bb_post_bedpostx_gpu_'
    # '${FSLDIR}/bin/fsl_sub -q ${QUEUE_MORE_MEM}  -N "bb_post_bedpostx_gpu_'
    # + subject_name
    # + '" -j '
    # + jobBEDPOSTX
    # + "  -l "
    # + log_dir
    # + "$BB_BIN_DIR/bb_diffusion_pipeline/bb_bedpostx/bb_post_bedpostx_gpu "
    # + base_dir
    # + "/dMRI/dMRI",
    # )

    #  running our own tractography algorithms so turning AutoPtx option off
    # lt.runCommand(
    # logger,
    # "$BB_BIN_DIR/bb_diffusion_pipeline/bb_autoPtx/bb_autoPtx "
    # + subject_name
    # + " "
    # + jobPOSTBEDPOSTX
    # + ","
    # + jobTBSS,
    # )

    logger.info("Running tvb_probtrackx...")
    lt.run_command(
        logger,
        "$BB_BIN_DIR/bb_diffusion_pipeline/tvb_probtrackx2/tvb_probtrackx2 " + base_dir,
        "tvb_probtrackx_" + subject_name,
    )
    logger.info("tvb_probtrackx completed.")

    # commenting out CPU version of probtrackx for now
    # jobPROBTRACKX = lt.runCommand(
    #     logger,
    #     base_dir
    #     + "/dMRI/probtrackx/probtrackx_commands_$SGE_TASK_ID.txt",
    #     "bb_probtrackx_"
    #     + subject_name
    # )
    # jobPROBTRACKX = jobPROBTRACKX.split(".")[0]

    logger.info("Running tvb_post_probtrackx...")
    job_post_probtrackx = lt.run_command(
        logger,
        "$BB_BIN_DIR/bb_diffusion_pipeline/tvb_probtrackx2/tvb_post_probtrackx2 "
        + subject,
        "tvb_post_probtrackx_" + subject_name,
    )
    logger.info("post_probrackx completed.")

    logger.info("Diffusion pipeline complete.")
    return job_post_probtrackx


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
    bb_pipeline_diff(subject_)
