#!/bin/env python

"""
 Authors: Fidel Alfaro Almagro
 FMRIB, Oxford University
 06-Apr-2019 18:03:23
 Version $1.0
 ProjectDir = 
 """

import os, sys, argparse

sys.path.insert(1, os.path.dirname(__file__) + "/..")
import bb_pipeline_tools.bb_logging_tool as LT
import bb_pipeline_tools.bb_file_manager as FM
import logging


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def bb_pipeline_FS(subject, jobHold, fileConfiguration):
    logger = logging.getLogger()
    logDir = logger.log_dir
    baseDir = logDir[0 : logDir.rfind("/logs/")]

    subname = subject.replace("/", "_")

    if (not "T1" in fileConfiguration) or (fileConfiguration["T1"] == ""):
        logger.error(
            "There is no T1. FreeSurfer for subject " + subject + " cannot be run."
        )
        LT.finish_logging(logger)
        return -1

    else:
        jobFS01 = LT.run_command(
            logger,
            "$BB_BIN_DIR/bb_FS_pipeline/bb_FS_run.sh  " + subject,
            "bb_FS_run_" + subname,
        )
        jobFS02 = LT.run_command(
            logger,
            "$BB_BIN_DIR/bb_FS_pipeline/bb_FS_segm.sh " + subject,
            "bb_FS_segm_" + subname,
        )
        jobFS03 = LT.run_command(
            logger,
            "$BB_BIN_DIR/bb_FS_pipeline/bb_FS_get_IDPs.py " + subject,
            "bb_FS_IDPs_" + subname,
        )

        LT.finish_logging(logger)
        return jobFS03


def main():
    parser = MyParser(description="BioBank FreeSurfer Tool")
    parser.add_argument("subjectFolder", help="Subject Folder")

    argsa = parser.parse_args()

    subject = argsa.subjectFolder
    subject = subject.strip()

    if subject[-1] == "/":
        subject = subject[0 : len(subject) - 1]

    fileConfig = FM.bb_file_manager(subject)

    bb_pipeline_FS(subject, "-1", fileConfig)

    print("SUBMITTED FS")
    print(jobSTEP1)


if __name__ == "__main__":
    main()
