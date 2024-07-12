#!/bin/env python
#

import numpy as np
import nibabel as nb

# import os
import sys, argparse, os.path
from subprocess import check_output


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main():
    parser = MyParser(description="get masks for probtrackx")
    parser.add_argument(
        "-i", dest="interface", type=str, nargs=1, help="Input_interface"
    )
    # parser.add_argument('-e', dest="exclude", type=str, nargs=1, help='Input_exclude')
    parser.add_argument(
        "-ri", dest="roied_interface", type=str, nargs=1, help="roied Interface"
    )
    # parser.add_argument('-re', dest='roied_exclude',type=str, nargs=1,help='roied exclude')
    parser.add_argument("-LUT", dest="LUT", type=str, nargs=1, help="LUT file")
    parser.add_argument(
        "-od", dest="output_dir", type=str, nargs=1, help="output directory"
    )

    argsa = parser.parse_args()

    if argsa.interface == None:
        parser.print_help()
        exit()

    # if (argsa.exclude==None):
    # parser.print_help()
    # exit()
    if argsa.roied_interface == None:
        parser.print_help()
        exit()
    # if (argsa.roied_exclude==None):
    # parser.print_help()
    # exit()

    Interface_inDTI = argsa.interface[0]
    # Exclude_inDTI = argsa.exclude[0]
    Interface_roied = argsa.roied_interface[0]
    # Exclude_roied = argsa.roied_exclude[0]
    LUT_file = argsa.LUT[0]
    out_dir = argsa.output_dir[0]
    print(Interface_inDTI)
    print(out_dir)

    Interface_roied_img = nb.load(Interface_roied)
    Interface_roied_data = Interface_roied_img.get_data()
    """roi_int = np.array(list(set(np.reshape(Interface_roied_data,\
        [Interface_roied_data.shape[0]*Interface_roied_data.shape[1]*Interface_roied_data.shape[2],]))))[1:]"""
    # Exclude_roied_img = nb.load(Exclude_roied)
    # Exclude_roied_data= Exclude_roied_img.get_data()
    # Interface_Exclude_roied_img = nb.load(Exclude_roied)
    Interface_inDTI_img = nb.load(Interface_inDTI)
    Interface_inDTI_data = Interface_inDTI_img.get_data()
    # Exclude_inDTI_img = nb.load(Exclude_inDTI)
    # Exclude_inDTI_data= Exclude_inDTI_img.get_data()

    # seed_ls=[None]*len(roi_int)
    f = open(LUT_file, "r")
    roi_int = []
    for line in f:
        roi_int.append(int(line.split("\t")[0]))
    f.close()
    # roi_int= list(range(2,43)) + list(range(51,54)) + list(range(61,65))+list(range(102,143)) + list(range(151,154)) + list(range(161,165))
    # exclude_intra_ls =[None]*len(roi_int)
    # exclude_ls =[None]*len(roi_int)
    seed_ls = [None] * len(roi_int)
    """all_msk_data = np.zeros_like(Interface_inDTI_data)
    all_exclude_data = np.zeros_like(Exclude_inDTI_data)
    all_mask_filename = 'roi_all_mask.nii.gz'
    all_exclude_filename = 'exclude_all_mask.nii.gz'"""
    for i in range(len(roi_int)):
        mask_filename = out_dir + "/roi_" + str(roi_int[i]) + "_mask.nii.gz"
        # exclude_filename = out_dir+'/exclude_'+str(roi_int[i])+'_mask.nii.gz'

        tmp_msk_data = np.zeros_like(Interface_inDTI_data)
        # tmp_exclude_data = np.zeros_like(Exclude_inDTI_data)

        tmp_msk_data[Interface_roied_data == roi_int[i]] = 1
        # tmp_exclude_data[Exclude_roied_data==roi_int[i]] =1

        tmp_msk_img = nb.Nifti1Image(
            tmp_msk_data, Interface_inDTI_img.affine, Interface_inDTI_img.header
        )
        nb.save(tmp_msk_img, mask_filename)
        # tmp_exclude_img = nb.Nifti1Image(tmp_exclude_data, Exclude_inDTI_img.affine, Exclude_inDTI_img.header)
        # nb.save(tmp_exclude_img, exclude_filename)

        seed_ls[i] = mask_filename
        # exclude_ls[i] = exclude_filename
        # seed_ls[i] = mask_filename
        # exclude_inter_ls[i] = exclude_filename

        """if roi_int[i] < 100:
            tmp_exclude_data[hemiL_inDTI_data > 0] =1
            tmp_exclude_intra_img = nb.Nifti1Image(tmp_exclude_data, Exclude_inDTI_img.affine, Exclude_inDTI_img.header)
            nb.save(tmp_exclude_intra_img, exclude_intra_filename)
        else:
            tmp_exclude_data[hemiR_inDTI_data > 0] =1
            tmp_exclude_intra_img = nb.Nifti1Image(tmp_exclude_data, Exclude_inDTI_img.affine, Exclude_inDTI_img.header)
            nb.save(tmp_exclude_intra_img, exclude_intra_filename)
            
        exclude_intra_ls[i] = os.path.abspath(exclude_intra_filename) """
        # exclude_intra_ls[i] = exclude_intra_filename

    file_seed = out_dir + "/seeds.txt"
    f = open(file_seed, "w+")
    for seed in seed_ls:
        f.write(seed + "\n")
    f.close()

    # file_stops=out_dir+'/stops.txt'
    # f= open(file_stops,"w+")
    # for seed in exclude_ls:
    #    f.write(seed+'\n')
    # f.close()
    # return seed_ls, exclude_ls


if __name__ == "__main__":
    main()
