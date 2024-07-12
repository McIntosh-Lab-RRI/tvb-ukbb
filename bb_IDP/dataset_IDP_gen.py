#!/bin/env python

import pandas as pd
import numpy as np
import sys
import os
import csv


def dataset_IDP_gen(BB_BIN_DIR, dataset, tvb_new_IDPs, ukbb_IDP_list):
    """Function that updates the ukbb_IDP_list txt file
    Parameters
    ----------
    BB_BIN_DIR: path to tvb pipeline tvb-ukbb


    """
    tvb_new_IDPs_data = list(csv.reader(open(tvb_new_IDPs), delimiter="\t"))
    ukbb_IDP_list_data = list(csv.reader(open(ukbb_IDP_list), delimiter="\t"))

    for row in tvb_new_IDPs_data[1:]:
        row = row[:-3]
        ukbb_IDP_list_data.append(row)

    outputfilename = os.path.join(BB_BIN_DIR, "bb_IDP", dataset + "_IDPs.tsv")
    with open(outputfilename, mode="w") as outputfile:
        writer = csv.writer(outputfile, delimiter="\t")

        writer.writerows(ukbb_IDP_list_data)


if __name__ == "__main__":
    """Function that updates the ukbb_IDP_list txt file.


    Usage
    ----------
    python  IDP_html_gen.py  IDP_list_path


    Arguments
    ----------


    BB_BIN_DIR: path to tvb pipeline tvb-ukbb


    dataset: name of dataset- e.g. Cam-CAN or ADNI3


    tvb_new_IDPs: file path to tvb new IDPs file


    ukbb_IDP_list: file path to ukbb IDP list file


    """
    # try:
    dataset_IDP_gen(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
