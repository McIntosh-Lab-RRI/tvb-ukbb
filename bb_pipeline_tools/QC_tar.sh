#!/bin/bash
#
# Script name: QC_tar.sh
#
# Description: Script to generate QC tars for portability 
#
# Usage: 
#         While in subjects folder:  QC_tar.sh subject_name group
#
## Author: Justin Wang


set -x
echo "$-"
set +e



if [[ -d "$2" ]]; then
    origDir="`pwd`/$2"
else
    origDir=`pwd`
fi


sub=$1

if [[ "$sub" =~ '/'$ ]]; then 
  sub=${sub%?}
fi


if [[ "$origDir" =~ '/'$ ]]; then 
  origDir=${origDir%?}
fi


sub_original=${sub}
sub=${sub}_QC
mv ${origDir}/${sub_original} ${origDir}/${sub}


if [[ "$1" == "" ]] ; then
    echo "Error: The selected subject does not exist"
    exit 0
fi




fMRI_files=""


ica_array=()
while IFS=  read -r -d $'\0'; do
    ica_array+=("$REPLY")
done < <(find ${origDir}/$sub/fMRI -maxdepth 1 -type d -name "*.ica" -print0)



#for each .ica file
for t in ${ica_array[@]}; do
	fMRI_ver=`basename $t`
	relative_path=$sub/fMRI/$fMRI_ver
	fMRI_files="$fMRI_files $relative_path/.files $relative_path/mc/trans.png $relative_path/mc/rot.png $relative_path/mc/disp.png $relative_path/filtered_func_data.ica/report $relative_path/report_log.html $relative_path/report_prestats.html $relative_path/report_reg.html $relative_path/report_unwarp.html $relative_path/report.html $relative_path/reg/highres2standard.png $relative_path/reg/example_func2highres.png $relative_path/reg/example_func2standard.png $relative_path/reg/example_func2standard1.png $relative_path/reg/unwarp/.ramp.gif $relative_path/reg/unwarp/.ramp2.gif $relative_path/reg/unwarp/EF_UD_shift+mag.png $relative_path/reg/unwarp/example_func_distorted2highres.png $relative_path/reg/unwarp/fieldmap2edges.png $relative_path/reg/unwarp/FM_UD_fmap_mag_brain2str.png $relative_path/reg/unwarp/FM_UD_sigloss+mag.png $relative_path/reg/unwarp/fmap+mag.png $relative_path/reg/unwarp/EF_UD_movie.gif $relative_path/reg/unwarp/EF_D_edges.gif $relative_path/reg/unwarp/EF_U_edges.gif"

done
 



feat_array=()
while IFS=  read -r -d $'\0'; do
    feat_array+=("$REPLY")
done < <(find ${origDir}/$sub/fMRI -maxdepth 1 -type d -name "*.feat" -print0)



#for each .feat file
for t in ${feat_array[@]}; do
	fMRI_ver=`basename $t`
	relative_path=$sub/fMRI/$fMRI_ver
	fMRI_files="$fMRI_files $relative_path/report_log.html $relative_path/report_poststats.html $relative_path/report_prestats.html $relative_path/report_reg.html $relative_path/report_stats.html $relative_path/report_unwarp.html $relative_path/report.html $relative_path/.files $relative_path/mc/trans.png $relative_path/mc/rot.png $relative_path/mc/disp.png $relative_path/reg/highres2standard.png $relative_path/reg/example_func2highres.png $relative_path/reg/example_func2standard.png $relative_path/reg/example_func2standard1.png $relative_path/reg/unwarp/EF_UD_shift+mag.png $relative_path/reg/unwarp/example_func_distorted2highres.png $relative_path/reg/unwarp/fieldmap2edges.png $relative_path/reg/unwarp/FM_UD_fmap_mag_brain2str.png $relative_path/reg/unwarp/FM_UD_sigloss+mag.png $relative_path/reg/unwarp/fmap+mag.png $relative_path/reg/unwarp/EF_UD_movie.gif $relative_path/reg/unwarp/EF_D_edges.gif $relative_path/reg/unwarp/EF_U_edges.gif $relative_path/reg/unwarp/.ramp2.gif $relative_path/reg/unwarp/.ramp.gif"

done

if [[ -d "$2" ]]; then
    cd ${2}
fi


tar --ignore-failed-read -cf $origDir/${sub}.tar $sub/QC* $sub/logs$fMRI_files $sub/IDP_files*/*.txt $sub/IDP_files*/*.tsv
#may need --ignore-failed-read option for non existent files/folders

if [[ -d "$2" ]]; then
    cd ..
fi

mv ${origDir}/${sub} ${origDir}/${sub_original}


set -e
 


