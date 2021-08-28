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

import os.path
import sys
import json

sys.path.insert(1, os.path.dirname(__file__) + "/..")
import bb_pipeline_tools.bb_logging_tool as LT


def bb_pipeline_func(subject, jobHold, fileConfiguration):

    # building blocks for more elaborate, generic design.fsf matching system
    # store old file paths in subject's fMRI directory

    subjDir = f"{os.getcwd()}/{subject}"

    f = open(subjDir + "/filenames.txt", "w")
    for k in fileConfiguration.keys():
        if "oldpath" in k:
            f.write(f"{k}:{fileConfiguration[k]}\n")
    f.close()

    logger = LT.initLogging(__file__, subject)
    logDir = logger.logDir
    baseDir = logDir[0 : logDir.rfind("/logs/")]

    jobsToWaitFor = ""

    subname = subject.replace("/", "_")

    jobPOSTPROCESS = LT.runCommand(
        logger,
        #'${FSLDIR}/bin/fsl_sub -T 5 -N "bb_postprocess_struct_'
        '${FSLDIR}/bin/fsl_sub -q ${QUEUE_STANDARD} -N "bb_postprocess_struct_'
        + subname
        + '" -l '
        + logDir
        + " -j "
        + str(jobHold)
        + " $BB_BIN_DIR/bb_functional_pipeline/bb_postprocess_struct "
        + subject,
    )

    rfMRI_nums = [
         k.split("_")[-1]
         for k in fileConfiguration.keys()
         if "rfMRI" in k and "oldpath" not in k and "SBRef" not in k
    ]

    # print(st)

    # print(f"rfMRI_nums:{rfMRI_nums}")
    # job for preparing fieldmap files
    jobGEFIELDMAP = LT.runCommand(
        logger,
        '${FSLDIR}/bin/fsl_sub -q ${QUEUE_STANDARD} -N "tvb_prepare_gradEchoFieldMap_'
        + subname
        + '" -l '
        + logDir
        + " -j "
        + str(jobPOSTPROCESS)
        + " $BB_BIN_DIR/bb_functional_pipeline/tvb_prepare_gradEchoFieldMap "
        + subject,
    )
    # if ("rfMRI" in fileConfiguration) and (fileConfiguration["rfMRI"] != ""):

    jobCLEAN_LAST_rfMRI = "-1"

    if len(rfMRI_nums) > 0:
        for i in range(len(rfMRI_nums)):
            # if it's the first rfMRI file start upon completion of fieldmap
            # otherwise use clean job ID from previous rfMRI iteration

            if i == 0:
                jobPREPARE_R = LT.runCommand(
                     logger,
                     #'${FSLDIR}/bin/fsl_sub -T 15   -N "bb_prepare_rfMRI_'
                     '${FSLDIR}/bin/fsl_sub -q ${QUEUE_STANDARD}   -N "bb_prepare_rfMRI_'
                     + f"{i}_{subname}"
                     + '"  -l '
                     + logDir
                     + " -j "
                     + jobGEFIELDMAP
                     + " $BB_BIN_DIR/bb_functional_pipeline/bb_prepare_rfMRI "
                     + subject
                     + f" {rfMRI_nums[i]}",
                 )
            else:
                jobPREPARE_R = LT.runCommand(
                     logger,
                     #'${FSLDIR}/bin/fsl_sub -T 15   -N "bb_prepare_rfMRI_'
                     '${FSLDIR}/bin/fsl_sub -q ${QUEUE_STANDARD}   -N "bb_prepare_rfMRI_'
                     + f"{i}_{subname}"
                     + '"  -l '
                     + logDir
                     + " -j "
                     + jobCLEAN_LAST_rfMRI
                     + " $BB_BIN_DIR/bb_functional_pipeline/bb_prepare_rfMRI "
                     + subject
                     + f" {rfMRI_nums[i]}",
                 )
            # TODO: Embed the checking of the fieldmap inside the independent steps -- Every step should check if the previous one has ended.
            #print(f"FILE CONFIG IN FUNC: {fileConfiguration}")
            #if ("rfMRI" in fileConfiguration) and (fileConfiguration["rfMRI"] != ""):

            
            jobFEAT_R = LT.runCommand(
                logger,
                #'${FSLDIR}/bin/fsl_sub -T 1200 -N "bb_feat_rfMRI_ns_'
                '${FSLDIR}/bin/fsl_sub -q ${QUEUE_MORE_MEM} -R 16000 -N "bb_feat_rfMRI_ns_'
                + f"{i}_{subname}"
                + '"  -l '
                + logDir
                + " -j "
                + jobPREPARE_R
                + " feat "
                + baseDir
                #
                # + f"/fMRI/rfMRI_{i}.fsf " + subject,
                + f"/fMRI/rfMRI_{i}.fsf",
            )
            jobFIX = LT.runCommand(
                logger,
                #'${FSLDIR}/bin/fsl_sub -T 175  -N "bb_fix_'
                '${FSLDIR}/bin/fsl_sub -q ${QUEUE_MAX_MEM}  -N "bb_fix_'
                + f"{i}_{subname}"
                + '"  -l '
                + logDir
                + " -j "
                + jobFEAT_R
                + " $BB_BIN_DIR/bb_functional_pipeline/bb_fix "
                + subject
                + f" {rfMRI_nums[i]}",
            )
            ### compute FC using parcellation
            jobFC = LT.runCommand(
                logger,
                '${FSLDIR}/bin/fsl_sub -q ${QUEUE_STANDARD} -N "bb_FC_'
                + f"{i}_{subname}"
                + '"  -l '
                + logDir
                + " -j "
                + jobFIX
                + " $BB_BIN_DIR/bb_functional_pipeline/bb_FC "
                + subject
                + f" {rfMRI_nums[i]}",
            )
            ### don't generate group-ICA RSNs
            # jobDR = LT.runCommand(
            # logger,
            ##'${FSLDIR}/bin/fsl_sub -T 120  -N "bb_ICA_dr_'
            #'${FSLDIR}/bin/fsl_sub -q ${QUEUE_MORE_MEM}  -N "bb_ICA_dr_'
            # + subname
            # + '"  -l '
            # + logDir
            # + " -j "
            # + jobFIX
            # + " $BB_BIN_DIR/bb_functional_pipeline/bb_ICA_dual_regression "
            # + subject,
            # )
            jobCLEAN = LT.runCommand(
                logger,
                #'${FSLDIR}/bin/fsl_sub -T 5  -N "bb_rfMRI_clean_'
                '${FSLDIR}/bin/fsl_sub -q ${QUEUE_STANDARD}  -N "bb_rfMRI_clean_'
                + f"{i}_{subname}"
                + '"  -l '
                + logDir
                + " -j "
                # + jobDR
                + jobFC
                + " $BB_BIN_DIR/bb_functional_pipeline/bb_clean_fix_logs "
                + subject
                + f" {rfMRI_nums[i]}",
            )

            jobCLEAN_LAST_rfMRI = jobCLEAN
            jobsToWaitFor += f"{jobCLEAN},"

    else:
        logger.error(
            "There is no rFMRI info. Thus, the Resting State part will not be run"
        )

    # if jobsToWaitFor != "":
    #     jobsToWaitFor += ","
    tfMRI_nums = [
        k.split("_")[-1]
        for k in fileConfiguration.keys()
        if "tfMRI" in k and "SBRef" not in k and "oldpath" not in k
    ]

    jobFEAT_LAST = "-1"

    # print(f"tfMRI_nums: {tfMRI_nums}")
    # if ("rfMRI" in fileConfiguration) and (fileConfiguration["rfMRI"] != ""):
    if len(tfMRI_nums) > 0:
        for i in range(len(tfMRI_nums)):
            # if ("tfMRI" in fileConfiguration) and (fileConfiguration["tfMRI"] != ""):
            if i == 0:
                jobPREPARE_T = LT.runCommand(
                    logger,
                    #'${FSLDIR}/bin/fsl_sub -T  15 -N "bb_prepare_tfMRI_'
                    '${FSLDIR}/bin/fsl_sub -q ${QUEUE_STANDARD} -N "bb_prepare_tfMRI_'
                    + f"{i}_{subname}"
                    + '" -l '
                    + logDir
                    + " -j "
                    + jobCLEAN_LAST_rfMRI
                    + " $BB_BIN_DIR/bb_functional_pipeline/bb_prepare_tfMRI "
                    + subject
                    + f" {tfMRI_nums[i]}",
                )
            else:
                jobPREPARE_T = LT.runCommand(
                    logger,
                    #'${FSLDIR}/bin/fsl_sub -T  15 -N "bb_prepare_tfMRI_'
                    '${FSLDIR}/bin/fsl_sub -q ${QUEUE_STANDARD} -N "bb_prepare_tfMRI_'
                    + f"{i}_{subname}"
                    + '" -l '
                    + logDir
                    + " -j "
                    + jobFEAT_LAST
                    + " $BB_BIN_DIR/bb_functional_pipeline/bb_prepare_tfMRI "
                    + subject
                    + f" {tfMRI_nums[i]}",
                )

            jobFEAT_T = LT.runCommand(
                logger,
                #'${FSLDIR}/bin/fsl_sub -T 400 -N "bb_feat_tfMRI_'
                '${FSLDIR}/bin/fsl_sub -q ${QUEUE_MORE_MEM} -R 16000 -N "bb_feat_tfMRI_'
                + f"{i}_{subname}"
                + '" -l '
                + logDir
                + " -j "
                + jobPREPARE_T
                + " feat  "
                + baseDir
                + f"/fMRI/tfMRI_{i}.fsf",
            )

            jobFEAT_LAST = jobFEAT_T

            if jobsToWaitFor != "":
                # jobsToWaitFor = jobsToWaitFor + "," + jobFEAT_T
                jobsToWaitFor += jobFEAT_T
            else:
                jobsToWaitFor = jobFEAT_T

    else:
        logger.error(
            "There is no tFMRI info. Thus, the Task Functional part will not be run"
        )

    if jobsToWaitFor == "":
        jobsToWaitFor = "-1"

    print("SUBMITTED FUNCTIONAL")

    os.rename(subjDir + "/filenames.txt", subjDir + "/fMRI/filenames.txt")
    return jobsToWaitFor


if __name__ == "__main__":
    # grab subject name from command
    subject = sys.argv[1]
    fd_fileName = "logs/file_descriptor.json"

    # check if subject directory exists
    if not os.path.isdir(subject):
        print(f"{subject} is not a valid directory. Exiting")
        sys.exit(1)
    # attempt to open the JSON file
    try:
        json_path = os.path.abspath(f"./{subject}/{fd_fileName}")
        with open(json_path, "r") as f:
            fileConfig = json.load(f)
    except:
        print(f"{json_path} could not be loaded. Exiting")
        sys.exit(1)
    # call pipeline
    bb_pipeline_func(subject, "-1", fileConfig)
