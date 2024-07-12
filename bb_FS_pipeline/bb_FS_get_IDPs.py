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
import logging


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def check_and_create_dir(dirName):
    try:
        os.stat(dirName)
    except:
        os.mkdir(dirName)


def read_file(fileName):
    result = []
    with open(fileName, "r") as f:
        for line in f.readlines():
            line = line.replace("\t", " ")
            result.append([x.replace("\n", "") for x in line.split(" ")])
    return result


def generate_FS_IDP_files(
    SUBJECTS_DIR, subject_ID, subject, dataDir, headersDir, logger
):
    os.environ["SUBJECTS_DIR"] = SUBJECTS_DIR
    statsDir = SUBJECTS_DIR + subject_ID + "/stats/"

    # TODO: Include a pre-rquisite that python2.7 must be availble in the system
    if os.path.isfile(statsDir + "aseg.stats"):
        LT.run_command(
            logger,
            "python2.7 $FREESURFER_HOME/bin/asegstats2table  "
            + " -m volume --all-segs --tablefile "
            + dataDir
            + "aseg_1.txt "
            + " --subjects "
            + subject_ID
            + " --skip",
            "FS_IDP_aseg_1_" + subject_ID,
        )
        LT.run_command(
            logger,
            "python2.7 $FREESURFER_HOME/bin/asegstats2table  "
            + " -m mean --all-segs --tablefile "
            + dataDir
            + "aseg_intensity.txt "
            + " --subjects "
            + subject_ID
            + " --skip",
            "FS_IDP_aseg_intensity_" + subject_ID,
        )

    if os.path.isfile(statsDir + "lh.w-g.pct.stats"):
        LT.run_command(
            logger,
            "python2.7 $FREESURFER_HOME/bin/asegstats2table "
            + " -m mean --all-segs --stats=lh.w-g.pct.stats "
            + " --tablefile "
            + dataDir
            + "wg_lh_mean.txt "
            + " --subjects "
            + subject_ID
            + " --skip",
            "FS_IDP_wg_lh_" + subject_ID,
        )

    if os.path.isfile(statsDir + "rh.w-g.pct.stats"):
        LT.run_command(
            logger,
            "python2.7 $FREESURFER_HOME/bin/asegstats2table "
            + " -m mean --all-segs --stats=rh.w-g.pct.stats "
            + " --tablefile "
            + dataDir
            + "wg_rh_mean.txt "
            + " --subjects "
            + subject_ID
            + " --skip",
            "FS_IDP_wg_rh_" + subject_ID,
        )

    for hemi in ["lh", "rh"]:
        for value in ["volume", "area", "thickness"]:
            for atlas in ["BA_exvivo", "aparc.DKTatlas", "aparc.a2009s", "aparc"]:
                outFileName = dataDir + atlas + "_" + hemi + "_" + value + ".txt"
                if os.path.isfile(statsDir + hemi + "." + atlas + ".stats"):
                    LT.run_command(
                        logger,
                        "python2.7 $FREESURFER_HOME/bin/aparcstats2table "
                        + " -m "
                        + value
                        + " --hemi="
                        + hemi
                        + " --tablefile "
                        + outFileName
                        + " --subjects "
                        + subject_ID
                        + " --skip -p "
                        + atlas,
                        "FS_IDP_hemi_" + subject_ID,
                    )

    atlas = "aparc.pial"
    value = "area"
    for hemi in ["lh", "rh"]:
        outFileName = dataDir + atlas + "_" + hemi + "_" + value + ".txt"
        if os.path.isfile(statsDir + hemi + ".aparc.pial.stats"):
            LT.run_command(
                logger,
                "python2.7 $FREESURFER_HOME/bin/aparcstats2table "
                + " -m "
                + value
                + " --hemi="
                + hemi
                + " --tablefile "
                + outFileName
                + " --subjects "
                + subject_ID
                + " --skip -p "
                + atlas,
                "FS_IDP_hemi_" + subject_ID,
            )

    with open(os.environ["BB_BIN_DIR"] + "/bb_data/FS_initial_files.txt") as f:
        files_generated = [x.replace("\n", "").split(" ") for x in f.readlines()]

    data_dict = {}

    for file_generated in files_generated:
        if os.path.isfile(dataDir + file_generated[0] + ".txt"):
            data = read_file(dataDir + file_generated[0] + ".txt")
        else:
            data = read_file(
                os.environ["BB_BIN_DIR"]
                + "/bb_data/FS_data_ex/"
                + file_generated[0]
                + ".txt"
            )
        data_dict[file_generated[0]] = data

    data_dict["ID"] = [["ID"], [subject]]

    return data_dict


# Quick consistency check
def check_consistency(data_dict):
    for file_generated in data_dict.keys():
        if len(data_dict[file_generated]) > 2:
            print("Error in " + file_generated + ": File has more than 2 lines")
            exit(-1)

        len0 = len(data_dict[file_generated][0])
        len1 = len(data_dict[file_generated][1])

        if len0 != len1:
            print("Error in " + file_generated + ": Inconsistent # of features")
            exit(-1)


def fix_aseg_data(data_dict, subjectDir):
    # Split aseg_1 into aseg_global and aseg_volume
    data_dict["aseg_global"] = [[], []]
    data_dict["aseg_global"][0] = [data_dict["aseg_1"][0][0]] + data_dict["aseg_1"][0][
        46:
    ]
    data_dict["aseg_global"][1] = [data_dict["aseg_1"][1][0]] + data_dict["aseg_1"][1][
        46:
    ]

    # Variables not needed
    vars_to_delete = [
        "CortexVol",
        "CerebralWhiteMatterVol",
        "SupraTentorialVolNotVentVox",
        "MaskVol",
        "SurfaceHoles",
    ]
    ind_to_delete = []
    for i in range(len(data_dict["aseg_global"][0])):
        if not (data_dict["aseg_global"][0][i] in vars_to_delete):
            ind_to_delete.append(i)

    data_dict["aseg_global"][0] = [
        data_dict["aseg_global"][0][x] for x in ind_to_delete
    ]
    data_dict["aseg_global"][1] = [
        data_dict["aseg_global"][1][x] for x in ind_to_delete
    ]

    # For some reason, the VentricleChoroidVol is not caught by asegstats2table
    try:
        with open(subjectDir + "/stats/aseg.stats", "r") as f:
            val = [
                x.split(",")[3].strip()
                for x in f.readlines()
                if "VentricleChoroidVol" in x
            ]
    except:
        val = ["NaN"]

    data_dict["aseg_global"][0].append("VentricleChoroidVol")
    data_dict["aseg_global"][1].append(val[0])

    data_dict["aseg_volume"] = [[], []]
    data_dict["aseg_volume"][0] = data_dict["aseg_1"][0][0:46]
    data_dict["aseg_volume"][1] = data_dict["aseg_1"][1][0:46]

    del data_dict["aseg_1"]

    # Remove the WM-hypointensities. No value in any subject
    cols_to_remove = [
        "Left-WM-hypointensities",
        "Right-WM-hypointensities",
        "Left-non-WM-hypointensities",
        "Right-non-WM-hypointensities",
    ]

    for key in list(data_dict.keys()):
        if key.startswith("aseg"):
            sub_keys_to_remove = []
            for sub_key in data_dict[key][0]:
                for col in cols_to_remove:
                    if col in sub_key:
                        sub_keys_to_remove.append(sub_key)

            for sub_key in sub_keys_to_remove:
                ind = data_dict[key][0].index(sub_key)
                del data_dict[key][0][ind]
                del data_dict[key][1][ind]

    return data_dict


def gen_aparc_special(data_dict, subjectDir):
    struct_data = []

    struct_data.append(
        ["aparc.pial_lh_area", "TotalSurface", "lh.aparc.pial.stats", "PialSurfArea"]
    )
    struct_data.append(
        ["aparc.pial_rh_area", "TotalSurface", "rh.aparc.pial.stats", "PialSurfArea"]
    )
    struct_data.append(
        ["aparc_lh_area", "TotalSurface", "lh.aparc.stats", "WhiteSurfArea"]
    )
    struct_data.append(
        ["aparc_rh_area", "TotalSurface", "rh.aparc.stats", "WhiteSurfArea"]
    )
    struct_data.append(
        ["aparc_lh_thickness", "GlobalMeanThickness", "lh.aparc.stats", "MeanThickness"]
    )
    struct_data.append(
        ["aparc_rh_thickness", "GlobalMeanThickness", "rh.aparc.stats", "MeanThickness"]
    )

    for elem in struct_data:
        data_dict[elem[0]][0].append(elem[1])
        try:
            with open(subjectDir + "/stats/" + elem[2], "r") as f:
                v = [x.split(",")[3].strip() for x in f.readlines() if elem[3] in x]
                data_dict[elem[0]][1].append(v[0])
        except:
            data_dict[elem[0]][1].append("NaN")

    return data_dict


def bool_FLAIR(data_dict, subjectDir):
    if os.path.isfile(subjectDir + "/mri/FLAIR.mgz"):
        data_dict["FLAIR"] = [["Use-T2-FLAIR-for-FreeSurfer"], ["1"]]
    else:
        data_dict["FLAIR"] = [["Use-T2-FLAIR-for-FreeSurfer"], ["0"]]

    return data_dict


def gen_subsegmentation(data_dict, subjectDir, subject):
    struct_data = {}
    struct_data["Brainstem_global"] = [["brainstemSsVolumes.v12.txt"], 5]
    struct_data["ThalamNuclei"] = [["ThalamicNuclei.v10.T1.volumes.txt"], 52]
    struct_data["AmygNuclei_lh"] = [
        ["lh.amygNucVolumes-T1-AN.v21.txt", "lh.amygNucVolumes-T1.v21.txt"],
        10,
    ]
    struct_data["AmygNuclei_rh"] = [
        ["rh.amygNucVolumes-T1-AN.v21.txt", "rh.amygNucVolumes-T1.v21.txt"],
        10,
    ]
    struct_data["HippSubfield_lh"] = [
        ["lh.hippoSfVolumes-T1-AN.v21.txt", "lh.hippoSfVolumes-T1.v21.txt"],
        22,
    ]
    struct_data["HippSubfield_rh"] = [
        ["rh.hippoSfVolumes-T1-AN.v21.txt", "rh.hippoSfVolumes-T1.v21.txt"],
        22,
    ]

    for struct in struct_data.keys():
        found = False
        data_dict[struct] = [[], []]
        for fil in struct_data[struct][0]:
            if os.path.isfile(subjectDir + "mri/" + fil):
                with open(subjectDir + "mri/" + fil, "r") as f:
                    for lin in f.readlines():
                        lin = lin.replace("\n", "").split(" ")
                        data_dict[struct][0].append(lin[0])
                        data_dict[struct][1].append(lin[1])
                found = True
                break

        if not found:
            with open(
                os.environ["BB_BIN_DIR"] + "/bb_data/FS_sub_headers/" + struct + ".txt"
            ) as f:
                data_dict[struct][0] = [x.replace("\n", "") for x in f.readlines()]
                data_dict[struct][0] = ["NaN"] * len(data_dict[struct][0])
        data_dict[struct][0] = ["ID"] + data_dict[struct][0]
        data_dict[struct][1] = [subject] + data_dict[struct][1]
    return data_dict


def fix_aparc_data(data_dict, subjectDir):
    # Remove the column "temporalpole" in aparc files.
    # Unreliable measure: Very few subjects have that measure.
    for key in list(data_dict.keys()):
        if key.startswith("aparc"):
            sub_keys_to_remove = []
            for sub_key in data_dict[key][0]:
                if "temporalpole" in sub_key:
                    sub_keys_to_remove.append(sub_key)
            for sub_key in sub_keys_to_remove:
                ind = data_dict[key][0].index(sub_key)

                if ind != -1:
                    del data_dict[key][0][ind]
                    del data_dict[key][1][ind]

    # Remove ETIV and BrainSegVolNotVent (They are global)
    for key in list(data_dict.keys()):
        if key.startswith("aparc") or key.startswith("BA_exvivo"):
            sub_keys_to_remove = []
            for sub_key in data_dict[key][0]:
                if sub_key in ["BrainSegVolNotVent", "eTIV"]:
                    sub_keys_to_remove.append(sub_key)
            for sub_key in sub_keys_to_remove:
                ind = data_dict[key][0].index(sub_key)
                del data_dict[key][0][ind]
                del data_dict[key][1][ind]

    # Removing last colum for thickness in aparc
    for key in list(data_dict.keys()):
        if key.startswith("aparc") and key.endswith("thickness"):
            sub_keys_to_remove = []
            for sub_key in data_dict[key][0]:
                if sub_key.endswith("MeanThickness_thickness"):
                    sub_keys_to_remove.append(sub_key)
            for sub_key in sub_keys_to_remove:
                ind = data_dict[key][0].index(sub_key)
                del data_dict[key][0][ind]
                del data_dict[key][1][ind]

    # Removing the last column for areas, also in BA
    for key in list(data_dict.keys()):
        if key.endswith("area"):
            sub_keys_to_remove = []
            for sub_key in data_dict[key][0]:
                if sub_key.endswith("WhiteSurfArea_area"):
                    sub_keys_to_remove.append(sub_key)
            for sub_key in sub_keys_to_remove:
                ind = data_dict[key][0].index(sub_key)
                del data_dict[key][0][ind]
                del data_dict[key][1][ind]

    return data_dict


# Remove first feature in case it is the subject ID (except for ID itself)
def remove_first_feature(data_dict, subject):
    for key in list(data_dict.keys()):
        if key != "ID":
            if (
                (data_dict[key][1][0] == subject)
                or (data_dict[key][1][0] == ("FS_" + subject))
                or (data_dict[key][1][0] == "")
            ):
                del data_dict[key][0][0]
                del data_dict[key][1][0]
    return data_dict


def fix_headers(data_dict):
    # Applying some general replacing rules for the categories
    replace_rules = [
        [".", "-"],
        ["BA_exvivo", "BA-exvivo"],
        ["AmygNuclei_lh", "AmygNuclei_lh_volume"],
        ["AmygNuclei_rh", "AmygNuclei_rh_volume"],
        ["Brainstem_global", "Brainstem_global_volume"],
        ["HippSubfield_lh", "HippSubfield_lh_volume"],
        ["HippSubfield_rh", "HippSubfield_rh_volume"],
        ["wg_lh_mean", "wg_lh_intensity-contrast"],
        ["wg_rh_mean", "wg_rh_intensity-contrast"],
        ["aparc_lh", "aparc-Desikan_lh"],
        ["aparc_rh", "aparc-Desikan_rh"],
        ["FLAIR", "Use-T2-FLAIR-for-FreeSurfer"],
    ]

    for key in list(data_dict.keys()):
        new_key = key
        for rule in replace_rules:
            if rule[0] in new_key:
                new_key = new_key.replace(rule[0], rule[1])
                data_dict[new_key] = data_dict.pop(key)

    # Renaming some special cases
    structs = [
        ["aseg_global", "lhSurfaceHoles", "aseg_lh_number", "HolesBeforeFixing"],
        ["aseg_global", "rhSurfaceHoles", "aseg_rh_number", "HolesBeforeFixing"],
        [
            "aseg_global",
            "BrainSegVol-to-eTIV",
            "aseg_global_volume-ratio",
            "BrainSegVol-to-eTIV",
        ],
        [
            "aseg_global",
            "MaskVol-to-eTIV",
            "aseg_global_volume-ratio",
            "MaskVol-to-eTIV",
        ],
    ]

    for struct in structs:
        index = data_dict[struct[0]][0].index(struct[1])
        if struct[2] not in data_dict.keys():
            data_dict[struct[2]] = [struct[3]], [data_dict[struct[0]][1][index]]
        else:
            data_dict[struct[2]][0].append(struct[3])
            data_dict[struct[2]][1].append(data_dict[struct[0]][1][index])
        del data_dict[struct[0]][0][index]
        del data_dict[struct[0]][1][index]

    for metric in ["volume", "intensity"]:
        old_key = "aseg_" + metric
        for i in range(len(data_dict[old_key][0])):
            if "Left-" in data_dict[old_key][0][i]:
                new_name = data_dict[old_key][0][i].replace("Left-", "")
                new_key = "aseg_lh_" + metric

                if new_key not in data_dict.keys():
                    data_dict[new_key] = [[], []]
                data_dict[new_key][0].append(new_name)
                data_dict[new_key][1].append(data_dict[old_key][1][i])
            elif "Right-" in data_dict[old_key][0][i]:
                new_name = data_dict[old_key][0][i].replace("Right-", "")
                new_key = "aseg_rh_" + metric

                if new_key not in data_dict.keys():
                    data_dict[new_key] = [[], []]
                data_dict[new_key][0].append(new_name)
                data_dict[new_key][1].append(data_dict[old_key][1][i])
            else:
                new_name = data_dict[old_key][0][i]
                new_key = "aseg_global_" + metric
                if new_key not in data_dict.keys():
                    data_dict[new_key] = [[], []]
                data_dict[new_key][0].append(new_name)
                data_dict[new_key][1].append(data_dict[old_key][1][i])

        del data_dict[old_key]

    for i in range(len(data_dict["aseg_global"][0])):
        if data_dict["aseg_global"][0][i].startswith("lh"):
            new_name = (
                data_dict["aseg_global"][0][i].replace("lh", "").replace("Vol", "")
            )
            data_dict["aseg_lh_volume"][0].append(new_name)
            data_dict["aseg_lh_volume"][1].append(data_dict["aseg_global"][1][i])
        elif data_dict["aseg_global"][0][i].startswith("rh"):
            new_name = (
                data_dict["aseg_global"][0][i].replace("rh", "").replace("Vol", "")
            )
            data_dict["aseg_rh_volume"][0].append(new_name)
            data_dict["aseg_rh_volume"][1].append(data_dict["aseg_global"][1][i])
        else:
            new_name = data_dict["aseg_global"][0][i].replace("Vol", "")
            data_dict["aseg_global_volume"][0].append(new_name)
            data_dict["aseg_global_volume"][1].append(data_dict["aseg_global"][1][i])

    del data_dict["aseg_global"]

    # Split ThalamNuclei into Left and Right
    data_dict["ThalamNuclei_lh_volume"] = [[], []]
    data_dict["ThalamNuclei_rh_volume"] = [[], []]
    for i in range(len(data_dict["ThalamNuclei"][0])):
        if "Left" in data_dict["ThalamNuclei"][0][i]:
            new_name = data_dict["ThalamNuclei"][0][i].replace("Left-", "")
            data_dict["ThalamNuclei_lh_volume"][0].append(new_name)
            data_dict["ThalamNuclei_lh_volume"][1].append(
                data_dict["ThalamNuclei"][1][i]
            )

        elif "Right" in data_dict["ThalamNuclei"][0][i]:
            new_name = data_dict["ThalamNuclei"][0][i].replace("Right-", "")
            data_dict["ThalamNuclei_rh_volume"][0].append(new_name)
            data_dict["ThalamNuclei_rh_volume"][1].append(
                data_dict["ThalamNuclei"][1][i]
            )
    del data_dict["ThalamNuclei"]

    # Removing redundant prefix and sufix in BA_excvivo
    BAs = ["_exvivo_area", "_exvivo_thickness", "_exvivo_volume"]
    BA_keys = [key for key in list(data_dict.keys()) if key.startswith("BA-exvivo")]
    for key in BA_keys:
        for i in range(len(data_dict[key][0])):
            for BA in BAs:
                data_dict[key][0][i] = (
                    data_dict[key][0][i]
                    .replace(BA, "")
                    .replace("rh_", "")
                    .replace("lh_", "")
                )

    # Removing redundant prefix and sufix in aparc
    aparcs = ["_area", "_thickness", "_volume", "-area", "-thickness", "-volume"]
    aparc_keys = [key for key in list(data_dict.keys()) if key.startswith("aparc")]
    for key in aparc_keys:
        for i in range(len(data_dict[key][0])):
            for aparc in aparcs:
                data_dict[key][0][i] = (
                    data_dict[key][0][i]
                    .replace(aparc, "")
                    .replace("rh_", "")
                    .replace("lh_", "")
                )

    # Changing weird and inconsistent characters
    for key in list(data_dict.keys()):
        for i in range(len(data_dict[key][0])):
            data_dict[key][0][i] = (
                data_dict[key][0][i].replace("_", "-").replace("&", "+")
            )

    return data_dict


def save_data(data_dict, SUBJECTS_DIR):
    with open(os.environ["BB_BIN_DIR"] + "/bb_data/FS_headers.txt") as f:
        final_headers = [x.replace("\n", "") for x in f.readlines()]

    temp_headers = {}

    for key in list(data_dict.keys()):
        if key in ["ID", "Use-T2-FLAIR-for-FreeSurfer"]:
            temp_headers[key] = data_dict[key][1][0]
        else:
            for i in range(len(data_dict[key][0])):
                temp_headers[key + "_" + data_dict[key][0][i]] = data_dict[key][1][i]

    for x in final_headers:
        if x not in temp_headers.keys():
            temp_headers[x] = "NaN"

    with open(SUBJECTS_DIR + "/IDP_files/FS_IDPs.txt", "w") as f:
        values = [temp_headers[x] for x in final_headers]
        values_str = " ".join(values)
        f.write("%s\n" % values_str)
        f.close()


def save_headers_info(data_dict, SUBJECTS_DIR):
    with open(os.environ["BB_BIN_DIR"] + "/bb_data/FS_final_headers.txt") as f:
        final_headers = [x.replace("\n", "") for x in f.readlines()]

    temp_headers = {}

    for key in list(data_dict.keys()):
        if key in ["ID", "Use-T2-FLAIR-for-FreeSurfer"]:
            temp_headers[key] = data_dict[key][1][0]
        else:
            for i in range(len(data_dict[key][0])):
                temp_headers[key + "_" + data_dict[key][0][i]] = data_dict[key][1][i]

    for x in final_headers:
        if x not in temp_headers.keys():
            temp_headers[x] = "NaN"

    with open(SUBJECTS_DIR + "/IDP_files/FS_headers_info.txt", "w") as f:
        values = [temp_headers[x] for x in final_headers]
        values_str = " ".join(values)
        f.write("%s\n" % values_str)

        f.close()


def bb_FS_get_IDPs(subject):
    logger = logging.getLogger()
    #    logger  = lt.initLogging('log', subject)
    logDir = logger.log_dir
    baseDir = logDir[0 : logDir.rfind("/logs/")]

    SUBJECTS_DIR = os.getcwd() + "/" + subject + "/"
    subject_ID = "FS_" + subject

    subjectDir = SUBJECTS_DIR + subject_ID + "/"

    if not os.path.isdir(subjectDir):
        subject_ID = "FreeSurfer"
        subjectDir = SUBJECTS_DIR + subject_ID + "/"
        if not os.path.isdir(subjectDir):
            print("Error: FreeSurfer has not been run on this subject")
            exit(-1)

    dataDir = SUBJECTS_DIR + subject_ID + "/data/"
    headersDir = SUBJECTS_DIR + subject_ID + "/headers/"

    check_and_create_dir(dataDir)
    check_and_create_dir(headersDir)

    data_dict = generate_FS_IDP_files(
        SUBJECTS_DIR, subject_ID, subject, dataDir, headersDir, logger
    )
    data_dict = fix_aseg_data(data_dict, subjectDir)
    data_dict = gen_aparc_special(data_dict, subjectDir)
    data_dict = gen_subsegmentation(data_dict, subjectDir, subject)
    data_dict = bool_FLAIR(data_dict, subjectDir)
    data_dict = fix_aparc_data(data_dict, subjectDir)
    data_dict = remove_first_feature(data_dict, subject)
    data_dict = fix_headers(data_dict)

    check_consistency(data_dict)
    save_data(data_dict, SUBJECTS_DIR)

    LT.finish_logging(logger)


def main():
    parser = MyParser(description="BioBank FreeSurfer IDP generation Tool")
    parser.add_argument("subjectFolder", help="Subject Folder")

    argsa = parser.parse_args()

    subject = argsa.subjectFolder
    subject = subject.strip()

    if subject[-1] == "/":
        subject = subject[0 : len(subject) - 1]

    if not os.path.isdir(subject):
        print("Error: The subject " + subject + " does not exist")
        exit(-1)

    bb_FS_get_IDPs(subject)


if __name__ == "__main__":
    main()
