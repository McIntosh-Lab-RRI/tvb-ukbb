#!/bin/bash
#
# Script name: subj_tar_batchcopy.sh
#
# Description: Script to batch generate subj tars for all processed subs and copy them into subj_tar
#
# Usage: 
#         While in subjects folder (you should see AD, CN, EMCI etc subdirs):  subj_tar_batchcopy.sh subjects_tsv
#
## Author: Justin Wang


set -x
echo "$-"
set +e
oridDir=`pwd`

mkdir subj_tar

# while IFS= read -r subjname; do
while IFS=$' \t\r\n' read -r subjname group; do
  mkdir subj_tar/${group}

  cd ${group}
  tar -czvf ${subjname}.tar.gz ${subjname}
  cd ..

  mv ${group}/${subjname}.tar.gz subj_tar/${group}/

done < "$1"


#may need --ignore-failed-read option for non existent files/folders


set -e