#!/bin/bash

# This script is for handling already processed subject T1s for VBM template creation.
# It extracts and renames T1s from an  subject's tarball into specified directory.
# It assumes each T1 is generically named (T1_orig.nii.gz) and renames with group and subject ID in destination directory
#
# usage:
#	extract_processed_t1s.sh source_directory destination_directory group subjID
#

source=$1
destination=$2
group=$3
subjID=$4

#TODO: add FOR loop to read list of subject IDs and group; need to also add option of different source directories for different subjects

tar -xvf "${source}/${group}/${subjID}.tar.gz" -C "${destination}/" "${subjID}/T1/T1_orig.nii.gz" 
mv "${destination}/${subjID}/T1/T1_orig.nii.gz" "${destination}/${group}_${subjID}_T1_orig.nii.gz"
rm -r "${destination}/${subjID}"



