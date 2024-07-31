#!/bin/env python
"""
Script name: bb_logging_tool.py

Description:

    A set of functions to do proper logging for python scripts.

    Logs are designed to reflect the linear design of the pipeline. The logger naming hierarchy is designed to reflect
    this is the logs themselves and the python logger objects. Logger names are determined by the current scripts base
    name. For example, at the highest level, the pipeline is defined and run from bb_pipeline_tools/bb_pipeline.py,
    where sub-pipelines are called. This results in a log file that looks like this:

        #todo: include example

    the naming in the log records reflects the pipeline call stack with bb_pipeline at the highest level of the main
    pipeline and all sub-pipelines and processes following in a similar manner. Retrieving the logger object in the
    sub-pipeline or sub-process files using the get_logger() ensures the integrity of this structure.

Authors:

        Fidel Alfaro-Almagro, Stephen M. Smith & Mark Jenkinson

Contributors:

        Patrick Mahon (pmahon@sfu.ca)

License:

    Copyright 2017 University of Oxford

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import os
import logging
import inspect
from subprocess import run
import shlex
import textwrap


def init_logging(subject):
    """
    Initializes the logging system for the given python file and subject.

    Args:
        subject: The name of the subject file being run.

    Returns:
        A python logger object.
    """
    log_file = f"logs/{subject}.log"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(module)s - %(filename)s - %(levelname)s - %(message)s",
    )

    logger = logging.getLogger()
    logger.log_dir = os.path.dirname(log_file)

    logging.info("Logging directory created at: " + os.getcwd() + "/" + log_file)

    return logger


def run_command(logger, command, job_name):
    """
    Performs the specified command and logs the resulting output.

    Args:
        logger:     The python logging object.
        command:    The command to be run.
        job_name:   The name of the current job.

    Returns:    None: Writes to corresponding log files specified by the logger object.
    """

    # Standard out/error printing indentation level
    indent_level = 4

    try:
        # resolve environment var filepaths and parse
        command_list = shlex.split(os.path.expandvars(command))

        logger.info("RUNNING:\n\t" + command.strip())

        # create logging directory for the calling module if it doesn't exist.
        calling_module = "/" + inspect.getmodule(inspect.stack()[1][0]).__name__ + "/"

        if not os.path.isdir(logger.log_dir + calling_module):
            os.mkdir(logger.log_dir + calling_module)

        # perform the designated commands and capture output
        std_out_file = (
            logger.log_dir + "/" + calling_module.split(".")[0] + "/" + job_name + ".o"
        )
        std_error_file = (
            logger.log_dir + "/" + calling_module.split(".")[0] + "/" + job_name + ".e"
        )

        os.makedirs(os.path.dirname(std_out_file), exist_ok=True)
        os.makedirs(os.path.dirname(std_error_file), exist_ok=True)

        std_out = open(std_out_file, "w+")
        std_error = open(std_error_file, "w+")

        jobOUTPUT=run(command_list, text=True, stdout=std_out, stderr=std_error)

        std_out.close()
        std_error.close()

        logger.info("STANDARD OUT: " + std_out_file)
        logger.info("STANDARD ERROR: " + std_error_file)

        logger.info("COMPLETE: " + command.strip())
        jobOUTPUT=jobOUTPUT.decode("UTF-8")
        
    except Exception as e:
        logger.error("Exception raised during execution of: \n\t" + command.strip())
        logger.error("Exception type: \n\t" + str(type(e)))
        logger.error("Exception args: \n\t" + str(e.args))
        logger.error("Exception message: \n\t" + str(e))
        jobOUTPUT = ""
        
    return jobOUTPUT.strip()
