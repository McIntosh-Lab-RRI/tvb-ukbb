"""
Python script to batch process subjects using the TVB-UK Biobank pipeline.

This script was written for old OGS/SGE systems where you can't just
submit 600 subjects and expect it to handle it properly. The script
allows you to specify a number of subjects to have running via
OGS/SGE at any given time.

Additional features of batching script:
    - Specify a number of subjects to submit to `qsub` concurrently.
    - Logs printed out in addition to printing into the terminal.
    - Resume function in the event the batch script ends abruptly.
    - Load text file with a subject name on each line and only run
        those subjects.
    - Resume from a session where the subjects were loaded in from
        a text file.
    - Marks subjects that completed successfully and subjects that
        errored out during the session.

Example setup:

    Subjects are in directory `/drive/subjects`. There's a text file,
    `/drive/subjects.txt`, containing the subject names to be run
    (one subject name per line). cd to /drive/subjects.
    In the conda env, run (on one line)

    > python <absolute_path_to_tvb-ukbb>/bb_pipeline_tools/tvb_pipeline_batch.py 
      -s . -n 3 --rotman --from-txt ../subjects.txt

    This line runs the batch script on the subject directories
    in the current directory, specifies 3 subjects to be run at
    once, and specifies the text file in the directory above the
    current one as the subject list to load in.

    Note: in this example, the logfile would be located in
          /drive/batch_2021XXXXXXXXXX (replace Xs with
          timestamp of when script was launched)
    
@author: Noah Frazier-Logue
"""

import sys
import os
import argparse
import time
import subprocess
import logging

from qstat import qstat
from datetime import datetime

# rename main function for clarity
import bb_logging_tool as LT
from bb_pipeline import main as bb_pipeline


def queuer(args):
    """
    Handles queuing of subjects and checking of statuses in `qsub`.

    Grabs initial queue state from `start_queue`. Checks state of
    queue via `qstat` every 30 seconds and replaces subjects as
    necessary. Prints and logs subject status every 15 minutes.
    When all subjects are completed, it exits.
    """

    # start queue and collect variables
    subject_dirs, subj_counter, pid_list, subjs_running = start_queue(args)
    rotman_avoid_comp98()
    # anchor time for checking and monitor timers
    start_time = time.time()

    while subj_counter <= len(subject_dirs):
        # wait 5 seconds between polling qstat
        wait_time_check = 30.0
        # 0.1 is lowest float val where it won't execute multiple times
        if wait_time_check - (time.time() - start_time) % wait_time_check < 0.1:
            # check for finished jobs
            pid_list, subjs_running, subj_counter = check_handle_job_finished(
                args, pid_list, subj_counter, subject_dirs, subjs_running
            )
            # check for errored out jobs
            pid_list, subjs_running, subj_counter = check_handle_job_errored(
                args, pid_list, subj_counter, subject_dirs, subjs_running
            )
            rotman_avoid_comp98()
        # wait 15 minutes between polling qstat
        wait_time_check_status = 900.0
        if (
            wait_time_check_status - (time.time() - start_time) % wait_time_check_status
            < 0.1
        ):
            # print running subjects status every 15 minutes
            print_subject_statuses(subjs_running)

    logger.info("All subjects completed.")
    print("All subjects completed.")


def start_queue(args):
    """
    Uses the parameters grabbed via `argparse` to initialize
    the queue and run the first few subjects.

    Submits first `args.num_concurrents` subjects (or fewer
    if there end up not being that many) and passes resulting
    queue state to `queuer`.

    Parameters
    ----------
    args : object
        Object containing each argument parsed by argparse.

    Returns
    -------
    subject_dirs : list
        List of subjects to be run.
    subj_counter : int
        Icremented `sub_counter` based on number of errored
        out subjects.
    pid_list : list
        Updated list with new PID(s) replacing old ones.
    subjs_running : list
        Updated list of running subjects.

    """

    if args.resume:
        subject_dirs, subj_counter = resume(args)
    elif args.from_txt:
        # grab subjects from passed in text file
        subject_dirs = load_subjects_from_txt(args.from_txt)
        # index that tracks index of earliest unsubmitted subject
        subj_counter = 0
    else:
        # directory (subject) names in subjects_path, sorted
        subject_dirs = [f.name for f in os.scandir(args.subjects_paths) if f.is_dir()]
        # index that tracks index of earliest unsubmitted subject
        subj_counter = 0

    # if there are fewer subjects to run than the set number of
    # subjects to run at a time, that value to the nubmer of
    # subjects remaining
    if len(subject_dirs) < args.num_concurrents:
        args.num_concurrents = len(subject_dirs)

    # empty list to hold PIDs for number of concurrent subjects on grid
    # filled with -1 by default
    pid_list = [-1] * args.num_concurrents
    # store subject names corresponding to pid_list values
    subjs_running = [""] * args.num_concurrents

    # tracks number of successfully submitted subjects
    num_submitted = 0
    # populate pid_list with IDP PIDs from each subject (IDP is last step
    # of pipeline for each subject, so when it's done the subject is done
    print(f"Submitting first {args.num_concurrents} subjects to grid...")
    logger.info(f"Submitting first {args.num_concurrents} subjects to grid...")
    while num_submitted < args.num_concurrents:
        # assign PID returned from running pipeline to corresponding index
        # in pid_list
        curr_pid = bb_pipeline([subject_dirs[subj_counter]])
        curr_subj = subject_dirs[subj_counter].strip("\n")
        # print in-progress file so resume can detect messed up subjects
        try:
            with open(
                f"{args.subjects_paths}/{curr_subj}/in_progress.txt",
                "w+",
            ) as f:
                pass
        # error handling in case the file can't be written out
        except:
            logger.warn(
                f"Unable to save out in_progess file for " f"subject {curr_subj}"
            )
            print(f"Unable to save out in_progress file for " f"subject {curr_subj}")
        # if subject failed to be submitted in pipeline code
        if curr_pid == "-1":
            # don't assign to pid_list and subjs_running
            logger.warn(
                f"{curr_subj} failed to submit. "
                "Skipping and submitting a new subject its place."
            )
            print(
                f"{curr_subj} failed to submit. "
                "Skipping and submitting a new subject its place."
            )
            # print errors.txt file so resume can detect messed up subjects
            try:
                with open(
                    f"{args.subjects_paths}/{curr_subj}/errors.txt",
                    "w+",
                ) as f:
                    f.write(f"Subject failed to submit")
                    pass
            # error handling in case the file can't be written out
            except:
                logger.warn(
                    f"Unable to save out errors.txt file for " f"subject {curr_subj}"
                )
                print(f"Unable to save out errors.txt file for " f"subject {curr_subj}")
        else:
            pid_list[subj_counter] = curr_pid
            subjs_running[subj_counter] = curr_subj
            num_submitted += 1
            print(f"Submitted {subjs_running[subj_counter]} to grid.")
            logger.info(f"Submitted {subjs_running[subj_counter]} to grid.")

        subj_counter += 1

    print(f"First {args.num_concurrents} subjects submitted.")
    logger.info(f"First {args.num_concurrents} subjects submitted.")

    print(
        "Entering queue monitoring mode. "
        "Subject status will be updated every 15 minutes."
    )
    logger.info(
        "Entering queue monitoring mode. "
        "Subject status will be updated every 15 minutes."
    )

    return (subject_dirs, subj_counter, pid_list, subjs_running)


def check_handle_job_finished(
    args, pid_list, subj_counter, subject_dirs, subjs_running
):
    """
    Check if the subjects running are finished. If they are, add new subjects
    to the queue and replace the finished ones with the new subjects.
    Also writes a `completed.txt` file to the subject's directory and
    calls script `tvb-ukbb/bb_pipeline_tools/QC_tar.sh` to tar the
    QC files for standalone use.

    Parameters
    ----------
    args : object
        Object containing each argument parsed by argparse.
    pid_list : list
        List of final process IDs for each subject, where the PID is
        the qsub PID of the final step in the pipeline.
    subj_counter : int
        Counts how many subjects have been submitted since the
        script started.
    subject_dirs : list
        List of subjects to be run.
    subjs_running : list
        List with names of subjects currently submitted to `qsub`.

    Returns
    ------
    pid_list : list
        Updated list with new PID(s) replacing old ones.
    subj_counter : int
        Icremented `sub_counter` based on number of completed
        subjects.
    subjs_running : list
        Updated list of running subjects.
    """

    # path for QC_tar script to be run on subject completion
    QC_tar_path = os.path.abspath(
        os.path.join(os.environ["BB_BIN_DIR"], "bb_pipeline_tools/QC_tar.sh")
    )

    for i in range(len(pid_list)):
        # qstat() returns two lists of dictionaries: one with jobs
        # runnning, one with jobs in queue. combining them into all_jobs
        queue_info, job_info = qstat()
        all_jobs = queue_info + job_info

        # check is the already submitted subject is still in the list of jobs
        # by seeing if subject PID is in values list of each dictionary
        # negated so if subject isn't done, value returns False
        pid_done = not any(
            # [subjs_running[i] in all_jobs[j].values() for j in range(len(all_jobs))]
            [pid_list[i] in all_jobs[j].values() for j in range(len(all_jobs))]
        )

        # if this subject's done, replace it with a new one and increment
        if pid_done:
            # call QC_tar script - arg 0 is script name, arg 1 is subj name,
            # arg 2 is directory containing subjs
            try:
                subprocess.call(
                    ["bash", f"{QC_tar_path}", f"{subjs_running[i]}", f"{os.getcwd()}"]
                )
            except:
                print("Error occurred whlie calling script QC_tar_path.sh")
            # write completion file for just completed subject
            try:
                with open(
                    f"{args.subjects_paths}/{subjs_running[i]}/completed.txt", "w+"
                ) as f:
                    pass
            # error handling in case the file can't be written out
            except:
                logger.info(
                    f"Unable to save out completion file for "
                    f"subject {subjs_running[i]}"
                )
                print(
                    f"Unable to save out completion file for "
                    f"subject {subjs_running[i]}"
                )

            # if only one subject, don't submit another
            # if args.num_concurrents == 1:
            #     logger.info(f"{subjs_running[i]} has completed.")
            #     print(f"{subjs_running[i]} has completed.")
            #     # return empty vals and subj_counter
            #     return ([], [], subj_counter + 1)
            #     # otherwise, submit another
            # else:
            if subj_counter >= len(subject_dirs):
                print(f"{subjs_running[i]} has completed. No more ubjects to run.")
                logger.info(
                    f"{subjs_running[i]} has completed. No more subjects to run."
                )
                return (pid_list, subjs_running, subj_counter + 1)

            else:
                logger.info(
                    f"{subjs_running[i]} has completed. Submitting "
                    f"{subject_dirs[subj_counter]} in its place."
                )
                print(
                    f"{subjs_running[i]} has completed. Submitting "
                    f"{subject_dirs[subj_counter]} in its place."
                )

            # submit next subject
            pid_list[i] = bb_pipeline([subject_dirs[subj_counter]])
            subjs_running[i] = subject_dirs[subj_counter]

            # write out in_progress file for resume checking
            try:
                with open(
                    f"{args.subjects_paths}/{subjs_running[i]}/in_progress.txt",
                    "w+",
                ) as f:
                    pass
            except:
                logger.info(
                    f"Unable to save out in_progess file for "
                    f"subject {subjs_running[i]}"
                )
                print(
                    f"Unable to save out in_progress file for "
                    f"subject {subjs_running[i]}"
                )

            # replace old subject with new and increment counter
            subj_counter += 1
            logger.info(f"Submitted {subjs_running[i]} to grid.")
            print(f"Submitted {subjs_running[i]} to grid.")

    return pid_list, subjs_running, subj_counter


def check_handle_job_errored(args, pid_list, subj_counter, subject_dirs, subjs_running):
    """
    Checks if the subjects running have errored out. If they have,
    adds new subjects to the queue and replace the errored ones with
    the new subjects. Also writes an `errors.txt` file to the subject's
    directory with the names of the jobs that errored out for that
    subject.

    Parameters
    ----------
    args : object
        Object containing each argument parsed by argparse.
    pid_list : list
        List of final process IDs for each subject, where the PID is
        the qsub PID of the final step in the pipeline.
    subj_counter : int
        counts how many subjects have been submitted since the
        script started.
    subject_dirs : list
        list of subjects to be run.
    subjs_running : list
        List with names of subjects currently submitted to `qsub`.

    Returns
    ------
    pid_list : list
        Updated list with new PID(s) replacing old ones.
    subj_counter : int
        Icremented `sub_counter` based on number of errored
        out subjects.
    subjs_running : list
        Updated list of running subjects.
    """
    for i in range(len(pid_list)):
        # qstat() returns two lists of dictionaries: one with jobs
        # runnning, one with jobs in queue. combining them into all_jobs
        queue_info, job_info = qstat()
        all_jobs = queue_info + job_info

        # grab names of errored out subjects' jobs
        errored_jobs = [
            all_jobs[j]["JB_name"]
            for j in range(len(all_jobs))
            if subjs_running[i] in all_jobs[j]["JB_name"]
            and all_jobs[j]["state"] == "Eqw"
        ]

        # if this subject's errored out, replace it with a new one and increment
        if len(errored_jobs) > 0:
            logger.info(
                f"{subjs_running[i]} has errored on job(s) {errored_jobs}. "
                f"Submitting {subject_dirs[subj_counter]} in its place."
            )
            print(
                f"{subjs_running[i]} has errored on job(s) {errored_jobs}. "
                f"Submitting {subject_dirs[subj_counter]} in its place."
            )

            pid_list[i] = bb_pipeline([subject_dirs[subj_counter]])
            # write errors.txt file for errored out subject
            try:
                with open(
                    f"{args.subjects_paths}/{subjs_running[i]}/errors.txt", "w+"
                ) as f:
                    for job in errored_jobs:
                        f.write(f"Errors in {job}")
            except:
                logger.info(
                    f"Unable to save out error file for subject {subjs_running[i]}"
                )
                print(f"Unable to save out error file for subject {subjs_running[i]}")

            subjs_running[i] = subject_dirs[subj_counter]
            subj_counter += 1
            logger.info(f"Submitted {subjs_running[i]} to grid.")
            print(f"Submitted {subjs_running[i]} to grid.")

        # submitted subject errored before submission completed
        elif pid_list[i] == "-1":
            # don't assign to pid_list and subjs_running
            logger.warn(
                f"{subjs_running[i]} failed to submit. "
                "Skipping and submitting a new subject its place."
            )
            print(
                f"{subjs_running[i]} failed to submit. "
                "Skipping and submitting a new subject its place."
            )
            # print errors.txt file so resume can detect messed up subjects
            try:
                with open(
                    f"{args.subjects_paths}/{subjs_running[i]}/errors.txt",
                    "w+",
                ) as f:
                    f.write(f"Subject failed to submit")
            # error handling in case the file can't be written out
            except:
                logger.warn(
                    f"Unable to save out errors.txt file for "
                    f"subject {subjs_running[i]}"
                )
                print(
                    f"Unable to save out errors.txt file for "
                    f"subject {subjs_running[i]}"
                )
            # increment subj_counter to run next subject
            subj_counter += 1
            pid_list[i] = bb_pipeline([subject_dirs[subj_counter]])
            subjs_running[i] = subject_dirs[subj_counter]

    return pid_list, subjs_running, subj_counter


def get_subject_statuses(subjs_running, queue_info, job_info):
    """
    Grabs subject statuses from `qstat`.

    Uses `qstat` module to query `qstat`. Iterates through list of
    dictionaries it returns and grabs running job for each subject.
    If no job is running, it shoes next job in queue for that subject.

    Parameters
    ----------
    subjs_running : list
        List with names of subjects currently submitted to `qsub`.
    queue_info : list
        List of dictionaries where each dictionary is a running
        job in `qsub`.
    job_info : list
        List of dictionaries where each dictionary is a queued job
        in `qsub`.

    Returns
    -------
    subj_statuses : list
        List of statuses for each subject in `subjs_running`.
    """
    # get step subject is on from queue_info
    subj_statuses = [""] * len(subjs_running)
    for i in range(len(subjs_running)):
        # if running, append current job name
        subj_running = False
        # qstat returns list of dictionaries with qstat attributes
        for dct in queue_info:
            if subjs_running[i] in dct["JB_name"]:
                subj_statuses[i] = f"{dct['JB_name']}"
                subj_running = True
                break
        # if not running, print next up pending job
        if not subj_running:
            for dct in job_info:
                if subjs_running[i] in dct["JB_name"]:
                    subj_statuses[i] = f"pending: {dct['JB_name']}"
                    break
    return subj_statuses


def print_subject_statuses(subjs_running):
    """
    Prints subject names and what step of the pipeline they're on.

    Grabs subject statuses from get_subject_statuses and prints
    them to the terminal and to the logger.
    """
    queue_info, job_info = qstat()

    # get step subject is on from queue_info
    subj_statuses = get_subject_statuses(subjs_running, queue_info, job_info)

    # print it all out
    print("Subjects currently running:")
    logger.info("Subjects currently running:")
    for i in range(len(subjs_running)):
        print(f"{subjs_running[i]}: {subj_statuses[i]}")
        logger.info(f"{subjs_running[i]}: {subj_statuses[i]}")


def rotman_avoid_comp98():
    """
    Check each pending job. If that job is queued on bigmem_16.q,
    use qalter to avoid node 'comp98' which causes errors.

    qalter -l h='!comp98' <jobID>
    """

    queue_info, job_info = qstat()
    for i in range(len(job_info)):
        # if "comp98" in job_info[i]["queue_name"]:
        if job_info[i]["queue_name"] != None and "comp98" in job_info[i]["queue_name"]:
            job_id = job_info[i]["JB_job_number"]
            subprocess.call(["qalter", "-l", "h='!comp98'", job_id])


def resume(args):
    """
    Function that handles resuming batch in the event of a disruption.

    Checks if it's resuming from a .txt file. If it is, load from txt.
    Otherwise, load subject names from all subdirectories of root dir.
    Function then checks whether all subjects are done, what status
    they were in before script ended last, etc. and then resumes based
    on the states it finds for each subject. Valid, un-run subjects
    are added to the list that the function returns and the incremented
    counter is as well.

    Parameters
    ----------
    args : object
        Object containing each argument parsed by argparse.

    Returns
    -------
    unfinished : list
        list of subject names that have not been processed by
        the script.
    counter : int
        counts how many subjects removed from the first the
        script was before it was interrupted.

    """

    # grab subject names
    if args.from_txt:
        subject_dirs = load_subjects_from_txt(args.from_txt)
    else:
        subject_dirs = [f.name for f in os.scandir(args.subjects_paths) if f.is_dir()]

    unfinished = []
    counter = 0

    # this means all subjects are done
    if counter == len(subject_dirs):
        logger.warn("All subjects already completed. Exiting")
        print("All subjects already completed. Exiting")
        sys.exit(0)

    # grab absolute path to subjects directory
    path_prefix = os.path.abspath(args.subjects_paths)
    for subj in subject_dirs:
        # paaths to status txt files
        subj_dir = f"{path_prefix}/{subj}/completed.txt"
        subj_progress = f"{path_prefix}/{subj}/in_progress.txt"
        subj_error = f"{path_prefix}/{subj}/errors.txt"
        # if completion file doesn't exist, add subject to unfinished list
        if not os.path.isfile(subj_dir) and not os.path.isfile(subj_error):
            unfinished.append(subj)
        # in_progress file exists, but other two don't
        # not added to list
        elif os.path.isfile(subj_progress) and (
            not os.path.isfile(subj_dir) or not os.path.isfile(subj_error)
        ):
            logger.warn(
                f"{subj} was not completed the last time this script was run. "
                f"Please reset the subject's directory before running it again."
            )
            print(
                f"{subj} was not completed the last time this script was run. "
                f"Please reset the subject's directory before running it again."
            )
        # keep set at 0 since the list doesn't incldue any already completed subjects
        # # if it does exist, increment the counter
        # else:
        #     counter += 1

    if len(unfinished) == 0:
        logger.warn("No subjects to run. Exiting")
        print("No subjects to run. Exiting")
        sys.exit(0)

    return (unfinished, counter)


def load_subjects_from_txt(txt_file):
    """
    Reads in txt file containing one subject name on each line passed in from
    commmand line and returns list of subjects

    Parameters
    ----------
    txt_file : str
        File path to txt file containing subject names.

    Returns
    -------
    subjects : list
        List of subject names.
    """

    f = open(txt_file, "r")
    subjects = f.readlines()

    for i in range(len(subjects)):
        subjects[i] = subjects[i].strip("\n")

    f.close()
    return subjects


def parse_args():
    """
    Parse arguments passed in via the command line.

    Returns
    -------
    args : object
        Object containing each argument parsed by argparse.
    """
    prog_name = "tvb_pipeline_batch"

    parser = argparse.ArgumentParser(
        prog=prog_name,
        usage=f"{prog_name} [options]",
        description="Python script to batch process subjects using the "
        "TVB-UK Biobank pipeline",
    )

    parser.add_argument(
        "-s",
        "--subjects_paths",
        type=str,
        help="Full path to directory containing subject directories.",
    )

    parser.add_argument(
        "-n",
        "--num_concurrents",
        type=int,
        help="Number of subjects allowed to be on the grid at any given time.",
    )

    parser.add_argument(
        "--resume",
        action="store_true",
        help="Pick up where you left off if the program errors out.",
    )

    parser.add_argument(
        "--rotman",
        action="store_true",
        help="Enable Rotman-specific options for the pipeline/grid.",
    )
    parser.add_argument(
        "--from-txt",
        type=str,
        help="Load list of names of subject directories. Must be valid file "
        "path and subject directories must be in same directory as where the "
        "script is being run.",
    )
    # add args to environment
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    # get parsed args
    args = parse_args()
    now = datetime.now()
    # date string for log directory name
    date_str = now.strftime("%Y%m%d%H%M%S")

    # make this visible to all functions in script for ease of use
    global logger

    # co-opt subject logging for batch script
    # create logging directories beforehand or it errors out
    subj_name = f"batch_{date_str}"
    os.mkdir(f"{os.getcwd()}/../{subj_name}")
    os.mkdir(f"{os.getcwd()}/../{subj_name}/logs")

    # start logger
    logger = LT.init_logging(__file__, f"{subj_name}")
    # start queuer
    queuer(args)
