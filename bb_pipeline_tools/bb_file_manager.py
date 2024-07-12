#!/bin/env python
#
# Script name: bb_file_manager.py
#
# Description: Script to do the organisation of the files of a new dataset
# 			   in UK Biobank file/directory format.
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
import sys
import logging
import nibabel as nib

from shutil import copyfile

sys.path.insert(1, os.path.dirname(__file__) + "/..")

import bb_general_tools.bb_path as bb_path
import bb_pipeline_tools.bb_logging_tool as lt

logger: logging.RootLogger

idealConfig = {}
fileConfig = {}


def format_file_config():
    result = ""
    for key in fileConfig:
        result = result + key + "\n"
        for value in fileConfig[key]:
            result = result + "  " + value + "\n"
    return result


def generate_sb_ref(orig_path, output_path):
    command_to_run = (
        os.environ["BB_BIN_DIR"]
        + "/bb_functional_pipeline/bb_generate_SBRef "
        + orig_path
        + " "
        + output_path
    )
    logger.warning("There was no SBRef data for the subject " + orig_path)
    logger.warning(
        "The SBRef data will be generated now using the middle point of the subject"
    )
    logger.warning("Command to run: " + command_to_run)
    lt.run_command(logger, command_to_run, "SBRef")


def remove_phase_info(file_name):
    result = re.sub("_[PH]|_[ph].", "", file_name)
    return result


def remove_coil_info(file_name):
    result = re.sub("_COIL[0-9]*_", "_", file_name)
    return result


def remove_echo_info(file_name):
    result = re.sub("_ECHO.*_", "_", file_name)
    return result


def rename_no_coil_echo_info(file_name):
    result = remove_coil_info(file_name)
    result = remove_echo_info(result)

    if file_name != result:
        move_file(file_name, result)

    return result


def read_json(file_name):
    result = {}

    if os.path.isfile(file_name):
        if bb_path.isImage(file_name):
            json_file_name = bb_path.removeImageExt(file_name) + ".json"

            if os.path.isfile(json_file_name):
                with open(json_file_name, "r") as f:
                    result = json.load(f)
    return result


def get_image_json_field(file_name, field):
    result = []
    json_dict = read_json(file_name)

    if json_dict != {}:
        result = json_dict[field]

    return result


def check_if_json_field_exists(file_name, field):
    json_dict = read_json(file_name)
    # return true if field is a key in json_dict
    if field in json_dict.keys():
        return True

    return False


def image_type_contains(file_name, desired_type):
    image_type = get_image_json_field(file_name, "ImageType")

    # 2 possible formats in the BIDS json file
    if isinstance(image_type, str):
        image_type = image_type.split("_")
    elif not isinstance(image_type, list):
        raise NameError(
            "The content of the json file associated with "
            + file_name
            + " is incorrect"
        )

    if desired_type in image_type:
        return True

    return False


def is_normalised(file_name):
    normed_siemens = image_type_contains(file_name, "NORM")
    normed_philips = check_if_json_field_exists(file_name, "PhilipsRescaleSlope")
    # if either is True, file is normalised
    return normed_siemens or normed_philips
    # return image_type_contains(fileName, "NORM")


def is_phase(file_name):
    return image_type_contains(file_name, "P")


def move_to(list_files, destination):
    for fileName in list_files:
        move_file(fileName, destination + fileName)


# Convert all the file names to upper case to avoid
# ambiguities (Extensions are always in lower case)
# Remove _ character at the beginning of the filename
def capitalize_and_clean(list_files):
    logger.info("File names changed to upper case.")
    for fileName in list_files:
        f_path, f_name = os.path.split(fileName)
        new_file_name = f_name.upper()
        if new_file_name.startswith("_"):
            new_file_name = new_file_name[1:]

        endings = [".NII.GZ", "BVAL", "BVEC", "JSON"]

        for ending in endings:
            if new_file_name.endswith(ending):
                new_file_name = new_file_name.replace(ending, ending.lower())

        full_new = f_path + "/" + new_file_name
        os.rename(fileName, full_new)


def move_file(old_path, new_path):
    # The file may be a json file and may have been moved previously
    if os.path.isfile(old_path):
        logger.info("File moved/renamed: " + old_path + " to " + new_path)
        # os.rename(oldPath, newPath)
        copyfile(old_path, new_path)

        # If there is an associated json, move it as well
        if bb_path.isImage(old_path):
            plain_orig_name = bb_path.removeImageExt(old_path)
            plain_new_name = bb_path.removeImageExt(new_path)

            if os.path.isfile(plain_orig_name + ".json"):
                # os.rename(plain_orig_name + ".json", plain_new_name + ".json")
                copyfile(plain_orig_name + ".json", plain_new_name + ".json")


def move_file_add_to_config(old_path, key, bool_append):
    if bool_append:
        move_file(old_path, idealConfig[key] + "/" + old_path)
        fileConfig[key].append(idealConfig[key] + "/" + old_path)
    else:
        move_file(old_path, idealConfig[key])
        fileConfig[key] = idealConfig[key]


def robust_sort(list_files):
    list_files.sort()
    final_list = copy.copy(list_files)
    alternate = []

    for fileName in list_files:
        rest = fileName[fileName.rfind("_") + 1 :]

        try:
            cad_numb = rest[: rest.find(".")]
            if cad_numb[-1] == "A":
                cad_numb = cad_numb[:-1]
            for phaseEnd in ["PH", "ph"]:
                if cad_numb == phaseEnd:
                    rest = fileName[fileName.rfind("_" + phaseEnd) - 2 :]
                    cad_numb = rest[: rest.find("_" + phaseEnd + ".")]

            numb = int(cad_numb)
            alternate.append(numb)
        except ValueError:
            logger.error(
                "Found a file with an improper name: "
                + fileName
                + " . It will be moved to the unclassified folder"
            )
            final_list.remove(fileName)

    new_list = [x for (y, x) in sorted(zip(alternate, final_list))]

    return new_list


# The flag parameter indicates whether this is T1 or T2_FLAIR
def manage_struct(list_files, flag):
    # listFiles = robustSort(listFiles)
    num_files = len(list_files)

    list_files = [rename_no_coil_echo_info(x) for x in list_files]

    # bool_norm = [is_normalised(x) for x in listFiles]
    # ignore normalization for now
    bool_norm = [True for _ in list_files]

    if not any(bool_norm):
        logger.error("There was not an intensity-normalized " + flag + ".")
        if flag == "T1":
            logger.error("It will not be possible to process the subject")
    else:
        index_last_norm = (num_files - list(reversed(bool_norm)).index(True)) - 1
        normalised_file_name = list_files[index_last_norm]
        move_file_add_to_config(normalised_file_name, flag, False)
        list_files.remove(normalised_file_name)
        bool_norm = bool_norm[:index_last_norm]

        if False in bool_norm:
            index_last_not_norm = (
                len(bool_norm)
                - list(reversed(bool_norm[:index_last_norm])).index(False)
            ) - 1

            if index_last_not_norm >= 0:
                not_normalised_file_name = list_files[index_last_not_norm]
                move_file_add_to_config(
                    not_normalised_file_name, flag + "_notNorm", False
                )
                list_files.remove(not_normalised_file_name)

    for fileName in list_files:
        # os.path.basename will not work on Windows
        move_file(fileName, "unclassified/" + os.path.basename(fileName))


# The flag parameter indicates whether this is resting or task fMRI
def manage_fmri(list_files, flag):
    # listFiles = robustSort(listFiles)
    num_files = len(list_files)
    dim = []

    list_files = [rename_no_coil_echo_info(x) for x in list_files]

    # Get the dimensions for all the fMRI images
    for file_name in list_files:
        epi_img = nib.load(file_name)
        dim.append(epi_img.get_header()["dim"][4])

    if num_files == 0:
        logger.warning("There was no " + flag + " FMRI data")

    elif num_files == 1:
        # If the only fMRI we have is the SBRef
        if dim[0] == 1:
            logger.error(
                "There was only SBRef data for the subject. There will be no "
                + flag
                + "fMRI processing"
            )
            move_file_add_to_config(list_files[0], flag + "_SBRef", False)

        # If we have fMRI data but no SBRef, we generate it.
        else:
            move_file_add_to_config(list_files[0], flag, False)
            generate_sb_ref(idealConfig[flag], idealConfig[flag + "_SBRef"])
            fileConfig[flag + "_SBRef"] = idealConfig[flag + "_SBRef"]

    elif num_files == 2:
        biggest_image_dim = max(dim)
        ind_biggest_image = dim.index(biggest_image_dim)
        ind_smallest_image = 1 - ind_biggest_image

        # If there is at least one proper fMRI image
        if biggest_image_dim > 1:
            move_file_add_to_config(list_files[ind_biggest_image], flag, False)

            # If the other image is an SBRef image
            if dim[ind_smallest_image] == 1:
                move_file_add_to_config(
                    list_files[ind_smallest_image], flag + "_SBRef", False
                )

            # If not, forget about it and generate and SBRef
            else:
                generate_sb_ref(idealConfig[flag], idealConfig[flag + "_SBRef"])
                fileConfig[flag + "_SBRef"] = idealConfig[flag + "_SBRef"]

        else:
            logger.error(
                "There was only SBRef data for the subject. There will be no "
                + flag
                + "fMRI processing"
            )
            move_file_add_to_config(list_files[num_files - 1], flag + "_SBRef", False)

    # If there are more than 2 rfMRI images, and at least one has more than one volume,
    # we will take the biggest one as the fMRI volume and generate take as SBRef the one
    # with the previous numeration. If that one is not a proper SBRef, generate it.
    elif max(dim) > 1:
        ind_biggest_image = dim.index(max(dim))
        move_file_add_to_config(list_files[ind_biggest_image], flag, False)

        file_name = list_files[ind_biggest_image]
        plain_file_name = bb_path.removeImageExt(file_name)

        ind = -1
        try:
            number = int(plain_file_name.split("_")[-1])

            for fileToCheck in list_files:
                # Check if the file with the previous numeration is in the list
                number_to_check = int(bb_path.removeImageExt(file_name).split("_")[-1])
                if number_to_check == (number - 1):
                    ind = list_files.index(fileToCheck)

        except ValueError:
            logger.error(
                "Unable to determine SBRef via numeric indexing. Generating SBRef."
            )

        # If there is a file with the file number that should correspond to this case
        if ind > 0:
            # If the file with the previous numeration is a SBREF file
            if dim[ind] == 1:
                move_file_add_to_config(list_files[ind], flag + "_SBRef", False)

            # If not, forget about it and generate a new one
            else:
                generate_sb_ref(idealConfig[flag], idealConfig[flag + "_SBRef"])
                fileConfig[flag + "_SBRef"] = idealConfig[flag + "_SBRef"]

        else:
            generate_sb_ref(idealConfig[flag], idealConfig[flag + "_SBRef"])
            fileConfig[flag + "_SBRef"] = idealConfig[flag + "_SBRef"]

    # There are several fMRI images but neither of them have more than one volume
    else:
        logger.error(
            "There was only SBRef data for the subject. There will be no "
            + flag
            + "fMRI processing."
        )
        move_file_add_to_config(list_files[num_files - 1], flag + "_SBRef", False)


def manage_dwi(list_files):
    # listFiles = robustSort(listFiles)
    list_files = [rename_no_coil_echo_info(x) for x in list_files]

    # ignore _ADC files from ADNI3
    for fpath in list_files:
        if "_ADC" in fpath:
            list_files.remove(fpath)

    sub_list_files_d = {}
    image_files_d = {}

    num_files = len(list_files)
    if num_files == 0:
        logger.error("There was no DWI data.  There will be no DWI processing.")

    else:
        # number of AP/PA directions detected
        num_ap = 0

        # increment num_ap if any AP/PA directions found
        for fl in list_files:
            if ".nii.gz" in fl and ("PA" in fl or "AP" in fl):
                num_ap += 1

        # use single-direction if only one direction found
        if num_ap <= 1:
            encoding_directions = ["dwi"]
            logger.info("Single-direction DWI detected.")
        # assume AP/PA otherwise
        else:
            encoding_directions = ["AP", "PA"]

        # Code needed for the inconsistency in the file names in Diffusion over the different phases
        if list_files[0].startswith("MB3"):
            sub_list_files_d["PA"] = [x for x in list_files if x.find("PA") != -1]
            image_files_d["PA"] = [
                x for x in sub_list_files_d["PA"] if bb_path.isImage(x)
            ]

            sub_list_files_d["AP"] = [
                x for x in list_files if x not in sub_list_files_d["PA"]
            ]
            image_files_d["AP"] = [
                x for x in sub_list_files_d["AP"] if bb_path.isImage(x)
            ]

        elif "dwi" in list_files[0] or "DWI" in list_files[0]:
            sub_list_files_d["dwi"] = [x for x in list_files if x.find("dwi") != -1]
            image_files_d["dwi"] = [
                x for x in sub_list_files_d["dwi"] if bb_path.isImage(x)
            ]

        else:
            for direction in encoding_directions:
                sub_list_files_d[direction] = [
                    x for x in list_files if x.find(direction) != -1
                ]
                image_files_d[direction] = [
                    x for x in sub_list_files_d[direction] if bb_path.isImage(x)
                ]
        try:
            for direction in encoding_directions:
                dim = []

                sub_list_files = sub_list_files_d[direction]
                image_files = image_files_d[direction]

                for fileName in image_files:
                    epi_img = nib.load(fileName)
                    dim.append(epi_img.get_header()["dim"][4])

                num_image_files = len(image_files)

                if num_image_files == 0:
                    raise Exception(
                        "There should be at least one DWI image in the "
                        + direction
                        + " direction with more than one volume. DWI data is not correct."
                        " There will be no diffusion processing."
                    )

                biggest_image_dim = max(dim)
                ind_biggest_image = dim.index(biggest_image_dim)

                # There is no proper DWI image
                if biggest_image_dim <= 1:
                    raise Exception(
                        "There should be at least one DWI image in the "
                        + direction
                        + " direction with more than one volume. DWI data is not correct."
                        " There will be no diffusion processing."
                    )

                if num_image_files > 1:
                    # Check if there is SBRef file for the direction
                    if dim.count(1) == 0:
                        logger.warning(
                            "There was no SBRef file in the "
                            + direction
                            + " direction."
                        )

                    # If there is at least one, take the last one.
                    else:
                        # Get the index of the last image with dimension = 1
                        index_sb_ref = (
                            num_image_files - list(reversed(dim)).index(1) - 1
                        )
                        move_file_add_to_config(
                            image_files[index_sb_ref], direction + "_SBRef", False
                        )

                # Take the biggest image in the selected direction and set it as the DWI image for that direction
                move_file_add_to_config(
                    image_files[ind_biggest_image], direction, False
                )

                # BVAL and BVEC files should have the same name as the image, changing the extension
                bval_file_name = (
                    bb_path.removeImageExt(image_files[ind_biggest_image]) + ".bval"
                )
                bvec_file_name = (
                    bb_path.removeImageExt(image_files[ind_biggest_image]) + ".bvec"
                )

                if (bval_file_name not in sub_list_files) or (
                    bvec_file_name not in sub_list_files
                ):
                    raise Exception(
                        "There should be 1 bval and 1 bvec file in "
                        + direction
                        + " direction. DWI data is not correct. There will be no"
                        " diffusion processing."
                    )

                move_file_add_to_config(bvec_file_name, direction + "_bvec", False)
                move_file_add_to_config(bval_file_name, direction + "_bval", False)

        # In case of any big error in the data, set DWI data as non-existent.
        except Exception as e:
            for key in ["AP", "AP_bval", "AP_bvec", "PA", "PA_bval", "PA_bvec"]:
                fileConfig[key] = ""
            logger.error(str(e))

        # Set the rest of the files as unclassified
        for fileName in list_files:
            if os.path.isfile(fileName):
                fpath, fname = os.path.split(fileName)
                # quick way to prevent dwi files from being copied into unclassified
                if not ("dwi" in fileName and "dwi" in fileConfig):
                    move_file(fileName, "unclassified/" + fname)


def manage_swi(list_files):
    # listFiles = robustSort(listFiles)
    num_files = len(list_files)

    if num_files <= 133:
        logger.error(
            "There should be at least 134 SWI files. Only "
            + str(num_files)
            + " found. There will be no SWI processing"
        )

    elif num_files > 134:
        logger.error(
            "The number of SWI files ("
            + str(num_files)
            + ") is incorrect. There will be no processing"
        )

    else:
        main_files = [x for x in list_files if ("_COIL_" in x)]

        for mainFile in main_files:
            list_files.remove(mainFile)

        for key in ["SWI_MAG_TE1", "SWI_MAG_TE2", "SWI_PHA_TE1", "SWI_PHA_TE2"]:
            fileConfig[key] = []

        # Classifying coil files
        for fileName in list_files:
            bool_phase = is_phase(fileName)
            # bool_phase= bb_path.removeImageExt(fileName).endswith('_PHA')
            bool_te1 = fileName.find("_ECHO1_") != -1

            if bool_phase:
                if bool_te1:
                    move_file_add_to_config(fileName, "SWI_PHA_TE1", True)
                else:
                    move_file_add_to_config(fileName, "SWI_PHA_TE2", True)

            else:
                if bool_te1:
                    move_file_add_to_config(fileName, "SWI_MAG_TE1", True)

                else:
                    move_file_add_to_config(fileName, "SWI_MAG_TE2", True)

        # Classifying SWI files
        # is_phase function does not work due to SWI acquisition not complying with standard
        # DICOM configuration and hence, dcm2niix does not get the phase properly
        not_norm_mag_files = [
            mainFile
            for mainFile in main_files
            if (
                (not is_normalised(mainFile))
                and (not (bb_path.removeImageExt(mainFile).endswith("_PH")))
            )
        ]

        if len(not_norm_mag_files) != 2:
            logger.warning(
                "There should be 2 not normalised SWI files. SWI data will not be processed"
            )
            for mainFile in main_files:
                if os.path.isfile(mainFile):
                    move_file(mainFile, "SWI/unclassified/" + mainFile)

        else:
            for notNormMagFile in not_norm_mag_files:
                if notNormMagFile.find("_ECHO1_") != -1:
                    move_file_add_to_config(
                        notNormMagFile, "SWI_TOTAL_MAG_notNorm", False
                    )
                else:
                    move_file_add_to_config(
                        notNormMagFile, "SWI_TOTAL_MAG_notNorm_TE2", False
                    )

                main_files.remove(notNormMagFile)

            for mainFile in main_files:
                # bool_phase=is_phase(mainFile)
                bool_phase = bb_path.removeImageExt(mainFile).endswith("_PH")
                bool_te1 = mainFile.find("_ECHO1_") != -1

                if bool_phase:
                    if bool_te1:
                        move_file_add_to_config(mainFile, "SWI_TOTAL_PHA", False)
                    else:
                        move_file_add_to_config(mainFile, "SWI_TOTAL_PHA_TE2", False)

                else:
                    if bool_te1:
                        move_file_add_to_config(mainFile, "SWI_TOTAL_MAG", False)

                    else:
                        move_file_add_to_config(mainFile, "SWI_TOTAL_MAG_TE2", False)


def bb_file_manager(subject_):
    global logger
    global idealConfig
    global fileConfig

    logger = logging.getLogger()

    ideal_config_file = os.environ["BB_BIN_DIR"] + "/bb_data/ideal_config.json"
    with open(ideal_config_file, "r") as f:
        idealConfig = json.load(f)

    directories = [
        "delete",
        "unclassified",
        "raw",
        "T1",
        "T2_FLAIR",
        "SWI",
        "SWI/PHA_TE1",
        "SWI/PHA_TE2",
        "SWI/MAG_TE1",
        "SWI/MAG_TE2",
        "SWI/unclassified",
        "dMRI",
        "dMRI/raw",
        "fMRI",
        "fieldmap",
        "logs",
    ]

    patterns_actions = [
        [["*.[^log]"], capitalize_and_clean],
        [["dicom", "DICOM"], move_to, "delete/"],
        [["*T1*.nii.gz", "*MPRAGE*.nii.gz", "*IR-FSPGR*.nii.gz"], manage_struct, "T1"],
        [["T2*FLAIR*.nii.gz", "*FLAIR*.nii.gz"], manage_struct, "T2"],
        [
            [
                "*FMRI*RESTING*.nii.gz",
                "MB8*RESTING*.nii.gz",
                "*TASK*REST*.nii.gz",
                "*task*rest*.nii.gz",
                "*epi_rest*.nii.gz",
                "*rsfMRI*.nii.gz",
                "*fcMRI*.nii.gz",
            ],
            manage_fmri,
            "rfMRI",
        ],
        [
            [
                "*fmri*task*.nii.gz",
                "*FMRI*TASK*.nii.gz",
                "MB8*TASK*.nii.gz",
                "*epi_movie*.nii.gz",
                "*epi_smt*.nii.gz",
            ],
            manage_fmri,
            "tfMRI",
        ],
        [["SWI*nii.gz"], manage_swi],
        [["DIFF_*", "MB3_*", "*dwi*.*", "*DWI*.*"], manage_dwi],
        [["SWI*.*"], move_to, "SWI/unclassified/"],
    ]

    os.chdir(subject_)
    fd_file_name = "logs/file_descriptor.json"

    # Check if the subject has already been managed
    if os.path.isfile(fd_file_name):
        with open(fd_file_name, "r") as f:
            fileConfig = json.load(f)

    else:
        for directory in directories:
            if not os.path.isdir(directory):
                os.mkdir(directory)

        # listFiles = glob.glob("*.*")
        list_f = glob.glob(os.getcwd() + "/**/*.*", recursive=True)
        list_f.sort()

        # Organize the files in sets
        for patterns_action in patterns_actions:
            patterns = patterns_action[0]
            action = patterns_action[1]
            args = patterns_action[2:]

            list_files = []
            for fileTy in patterns:
                list_files.extend(
                    [
                        x
                        for x in glob.glob(
                            os.getcwd() + "/**/" + fileTy, recursive=True
                        )
                        if x not in list_files
                    ]
                )
            logger.info(
                "Performing action "
                + action.__name__
                + " on files with patterns "
                + str(patterns)
            )

            action(list_files, *args)

        # Create file descriptor
        logger.info(f"FILECONFIG:\n\t{fileConfig}")
        fd = open(fd_file_name, "w")
        json.dump(fileConfig, fd, sort_keys=True, indent=4, separators=(",", ": "))
        fd.close()

    os.chdir("..")

    return fileConfig


if __name__ == "__main__":
    # run bb_file_manager on subject
    subject = sys.argv[1]
    bb_file_manager(subject)
