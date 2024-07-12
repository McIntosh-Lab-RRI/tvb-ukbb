#!/bin/env python
#
# Script name: SC_FC.py
#
# Description: Script to generate SC, FC, TL, TS plots for QC html report.
#
## Author: Justin Wang

import numpy as np
import sys
from scipy.stats import zscore
import matplotlib.pyplot as plt
import matplotlib
import os
import copy

# increasing font size for plots
font = {"size": 100}
matplotlib.rc("font", **font)



def SC_FC(subj, subjName, PARC_NAME):
    """Function that generates SC, FC, TL, TS plots for QC html report
    for a subject.

    TODO: more error handling here and in function def to deal with
            invalid files and paths

    Parameters
    ----------
    subj : string
        Full path to subject's directory.


    subjName :
        Subject name.
    """

    # remove trailing forward slashes in subject paths
    if subj.endswith("/"):
        subj = subj[:-1]

    if not os.path.exists(subj + "/QC/SC_FC/"):
        os.makedirs(subj + "/QC/SC_FC/")

    f, ax1, ax2, ax3, ax4, ax5, ax6 = "", "", "", "", "", "", ""

    # import data and generate graphs for fMRI
    # for each ica folder in fMRI
    try:
        for file in sorted(os.listdir(subj + "/fMRI/")):
            if file.endswith(".ica"):

                # import FC and TS data
                fc_path = os.path.join(
                    subj + "/fMRI/", file, "fc_" + PARC_NAME + ".txt"
                )
                ts_path = os.path.join(
                    subj + "/fMRI/", file, "ts_" + PARC_NAME + ".txt"
                )

                FC = ""
                norm_ts = ""

                try:
                    FC = np.loadtxt(fc_path)
                    norm_ts = zscore(np.loadtxt(ts_path))
                    # norm_ts=np.loadtxt(subj + '/fMRI/rfMRI_0.ica/norm_ts.txt');

                except:
                    print("ERROR: fc, ts file not found")

                # generate plots for FC and TS
                try:
                    file_name_no_period = file.replace(".", "_")

                    # set range of -0.5 and 1 for FC values
                    FC_matrix = copy.deepcopy(FC)
                    for i in range(FC.shape[0]):
                        for j in range(FC.shape[1]):
                            if FC[i][j] < -0.5:
                                FC_matrix[i][j] = -0.5
                            if FC[i][j] > 1:
                                FC_matrix[i][j] = 1

                    # save matrix for FC
                    f, ax = plt.subplots(1, 1, figsize=(50, 50))
                    ax.set_title(file_name_no_period + " FC (linear scale)")
                    ax.set_xlabel("ROI")
                    ax.set_ylabel("ROI")
                    im = ax.imshow(FC_matrix, cmap="jet")
                    cbar = f.colorbar(im, ax=ax)
                    cbar.set_label("pearson correlation coefficient", rotation=270)

                    plt.tight_layout()
                    saveNm = (
                        subj
                        + "/QC/SC_FC/"
                        + subjName
                        + "_"
                        + file_name_no_period
                        + "_FC.png"
                    )
                    f.savefig(saveNm)

                    # save carpet plot for TS
                    f, ax = plt.subplots(1, 1, figsize=(50, 30))
                    ax.set_xlabel("volume")
                    ax.set_ylabel("ROI")
                    ax.set_title(file_name_no_period + " ROI timeseries carpet plot")
                    im = ax.imshow(norm_ts.transpose(), cmap="gray", aspect="auto")

                    plt.tight_layout()
                    saveNm = (
                        subj
                        + "/QC/SC_FC/"
                        + subjName
                        + "_"
                        + file_name_no_period
                        + "_carpet.png"
                    )
                    f.savefig(saveNm)

                    # save histogram for FC
                    f, ax = plt.subplots(1, 1, figsize=(50, 30))
                    ax.set_title(file_name_no_period + " FC histogram (linear scale)")
                    ax.set_xlabel("pearson correlation coefficient")
                    ax.set_ylabel("number of connections")
                    f = plt.hist(FC.ravel(), bins=100)
                    saveNm = (
                        subj
                        + "/QC/SC_FC/"
                        + subjName
                        + "_"
                        + file_name_no_period
                        + "_FC_hist.png"
                    )
                    plt.savefig(saveNm)

                except:
                    print("ERROR: can't generate graph for " + file)
    except:
        print("ERROR: no fMRI folder in subject directory")

    # import SC data
    SC = ""
    try:

        SC = np.loadtxt(subj + "/dMRI/sc_" + PARC_NAME + ".txt")
    except:
        print("ERROR: sc file not found")

    # import TL data
    tract_lengths = ""
    try:

        tract_lengths = np.loadtxt(subj + "/dMRI/distance_" + PARC_NAME + ".txt")
    except:
        print("ERROR: distance file not found")

    # generate graphs for SC
    try:
        SC_log = np.log10(SC)

        # set range of -6 and 0 for SC log values
        SC_log_matrix = copy.deepcopy(SC_log)
        for i in range(SC_log.shape[0]):
            for j in range(SC_log.shape[1]):
                if SC_log[i][j] < -6:
                    SC_log_matrix[i][j] = -6
                if SC_log[i][j] > 0:
                    SC_log_matrix[i][j] = 0

        # save matrix for SC
        f, ax = plt.subplots(1, 1, figsize=(50, 50))

        ax.set_xlabel("ROI")
        ax.set_ylabel("ROI")
        ax.set_title("SC (log scale)")
        ax.set_facecolor("#000000")
        im = ax.imshow(SC_log_matrix, cmap="CMRmap")
        cbar = f.colorbar(im, ax=ax)
        cbar.set_label("probability of connection (log10)", rotation=270)

        plt.tight_layout()
        saveNm = subj + "/QC/SC_FC/" + subjName + "_SC.png"
        f.savefig(saveNm)

        # save histogram for SC
        f, ax = plt.subplots(1, 1, figsize=(50, 30))

        ax.set_xlabel("probability of connection (log10)")
        ax.set_ylabel("number of connections")

        ax.set_title("SC histogram (log scale, -inf removed)")
        SC_log = SC_log[SC_log > float("-inf")]
        f = plt.hist(SC_log.ravel(), bins=100)
        saveNm = subj + "/QC/SC_FC/" + subjName + "_SC_hist.png"
        plt.savefig(saveNm)

    except:
        print("ERROR: Can't create SC graph")

    # generate graphs for TL
    try:
        tract_lengths_log = np.log10(tract_lengths)

        # set range of 0 and 2.5 for SC log values
        tract_lengths_log_matrix = copy.deepcopy(tract_lengths_log)
        for i in range(tract_lengths_log.shape[0]):
            for j in range(tract_lengths_log.shape[1]):
                if tract_lengths_log[i][j] < 0:
                    tract_lengths_log_matrix[i][j] = 0
                if tract_lengths_log[i][j] > 2.5:
                    tract_lengths_log_matrix[i][j] = 2.5

        # save matrix for TL
        f, ax = plt.subplots(1, 1, figsize=(50, 50))

        ax.set_xlabel("ROI")
        ax.set_ylabel("ROI")
        ax.set_title("tract length (log scale)")
        ax.set_facecolor("#000000")
        im = ax.imshow(tract_lengths_log_matrix, cmap="CMRmap")
        cbar = f.colorbar(im, ax=ax)
        cbar.set_label("tract length (log10 mm)", rotation=270)

        plt.tight_layout()
        saveNm = subj + "/QC/SC_FC/" + subjName + "_TL.png"
        f.savefig(saveNm)

        # save histogram for TL
        f, ax = plt.subplots(1, 1, figsize=(50, 30))

        ax.set_xlabel("tract length (mm)")
        ax.set_ylabel("number of tracts")

        ax.set_title("tract length histogram (linear scale, zeroes removed)")
        tract_lengths = tract_lengths[tract_lengths != 0]
        f = plt.hist(tract_lengths.ravel(), bins=100)
        saveNm = subj + "/QC/SC_FC/" + subjName + "_TL_hist.png"
        plt.savefig(saveNm)

    except:
        print("ERROR: Can't create TL graph")


if __name__ == "__main__":
    """Function that generates SC, FC, TL, TS plots for QC html report
    for a subject.


    Usage
    ----------
    python  SC_FC.py  subj


    Arguments
    ----------
    subj :
        Full path to subject's directory.


    subjName :
        Subject name.

    """
    # try:

    SC_FC(sys.argv[1], sys.argv[2], sys.argv[3])
