#!/bin/bash




label_underlay_flag=0
underlay_cmap="greyscale"
overlay=""
overlay_args=""
flag=0

alpha=25.0
cmap=red-yellow
modulateMax=1.0
secondOverlayflag=0
secondOverlay=""
secondOverlayColor=""
secondOverlayAlpha=25.0

label_or_volume_first="volume"
label_or_volume_second="volume"

xlimit=10
ylimit=10
zlimit=10
brightness_var=49.152368365123955
contrast_var=49.90029860765409


while getopts ":o:a:p:s:h:i:j:k:x:y:z:b:c:q:" opt; do
  case $opt in
    o)		#overlay file
      overlay=$OPTARG
      flag=1
      ;;
    
    a)		#overlay alpha value
      alpha=$OPTARG
      flag=1
      ;;
    p)		#overlay cmap value
      cmap=$OPTARG
      
      flag=1
      ;;

    
    s)
	  secondOverlay=$OPTARG
      secondOverlayflag=1
      flag=1
      ;;
    h)
	  secondOverlayColor=$OPTARG
      secondOverlayflag=1
      flag=1
      ;;
    i)
	  secondOverlayAlpha=$OPTARG
      secondOverlayflag=1
      flag=1
      ;;
    j)
    label_or_volume_first=$OPTARG
      flag=1
      ;;
    k)
    label_or_volume_second=$OPTARG
      secondOverlayflag=1
      flag=1
      ;;
    b)
    brightness_var=$OPTARG
      ;;
    c)
    contrast_var=$OPTARG
      ;;
    x)
    xlimit=$OPTARG
    ;;
    y)
    ylimit=$OPTARG
    ;;
    z)
    zlimit=$OPTARG
    ;;
    q)
    underlay_cmap=$OPTARG
    label_underlay_flag=1
    ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac


done
shift "$((OPTIND-1))"

if [ "$flag" -eq "1" ]; then
	if [ "$overlay" = "" ]; then
		echo "ERROR: Overlay display options require overlay option and overlay argument (-o)." >&2
     	exit 1
	fi
fi


if [ "$secondOverlayflag" -eq "1" ]; then
	if [ "$secondOverlay" = "" ]; then
		echo "ERROR: Second Overlay display options require overlay option and overlay argument (-o)." >&2
     	exit 1
	fi
fi


underlay=$1


first_overlay_template=""
if [ "$label_or_volume_first" = "volume" ]; then
  first_overlay_template="--overlayType volume --alpha $alpha --brightness 49.75000000000001 --contrast 49.90029860765409 --cmap $cmap --negativeCmap greyscale --gamma 0.0 --cmapResolution 256 --interpolation none --numSteps 100 --blendFactor 0.1 --smoothing 0 --resolution 100 --numInnerSteps 10 --clipMode intersection --volume 0"
else
  first_overlay_template="--overlayType label --alpha $alpha --brightness 49.75000000000001 --contrast 49.90029860765409 --lut $cmap --outlineWidth 1 --volume 0"
fi


second_overlay_template=""
if [ "$label_or_volume_second" = "volume" ]; then
  second_overlay_template="--overlayType volume --alpha $secondOverlayAlpha --brightness 49.75000000000001 --contrast 49.90029860765409 --cmap $secondOverlayColor --negativeCmap greyscale --gamma 0.0 --cmapResolution 256 --interpolation none --numSteps 100 --blendFactor 0.1 --smoothing 0 --resolution 100 --numInnerSteps 10 --clipMode intersection --volume 0"
else
  second_overlay_template="--overlayType label --alpha $secondOverlayAlpha --brightness 49.75000000000001 --contrast 49.90029860765409 --lut $secondOverlayColor --outlineWidth 1 --volume 0"
fi


declare -a axisNames 
axisNames[0]=sagittal
axisNames[1]=coronal
axisNames[2]=axial


subject_folder=$2

  dim1=`${FSLDIR}/bin/fslval $subject_folder$underlay dim1`
  dim2=`${FSLDIR}/bin/fslval $subject_folder$underlay dim2`
  dim3=`${FSLDIR}/bin/fslval $subject_folder$underlay dim3`
  pixdim1=`${FSLDIR}/bin/fslval $subject_folder$underlay pixdim1`
  pixdim2=`${FSLDIR}/bin/fslval $subject_folder$underlay pixdim2`
  pixdim3=`${FSLDIR}/bin/fslval $subject_folder$underlay pixdim3`
  dim1=$(echo "scale=4;$dim1 * $pixdim1" | bc)
  dim2=$(echo "scale=4;$dim2 * $pixdim2" | bc)
  dim3=$(echo "scale=4;$dim3 * $pixdim3" | bc)

  startingx=$(echo "scale=4;$dim1 * $xlimit/100" | bc) #`$(($dim1*$xlimit/100)) | bc` #10 #50
  endingx=$(echo "scale=4;$dim1 * (100-$xlimit)/100" | bc)  #$(($dim1*$((100-$xlimit))/100)) #95 #130
  startingy=$(echo "scale=4;$dim2 * $ylimit/100" | bc) #$(($dim2*$ylimit/100)) #10 #75
  endingy=$(echo "scale=4;$dim2 * (100-$ylimit)/100" | bc) #$(($dim2*$((100-$ylimit))/100)) #95 #160
  startingz=$(echo "scale=4;$dim3 * $zlimit/100" | bc) #$(($dim3*$zlimit/100)) #10 #75
  endingz=$(echo "scale=4;$dim3 * (100-$zlimit)/100" | bc) #$(($dim3*$((100-$zlimit))/100)) #65 #135

  

  declare -a sliceSpacing 
  sliceSpacing[0]=$(echo "scale=4;($endingx-$startingx)/17 + 1" | bc)
  sliceSpacing[1]=$(echo "scale=4;($endingy-$startingy)/17 + 1" | bc)
  sliceSpacing[2]=$(echo "scale=4;($endingz-$startingz)/17 + 1" | bc)
 

  sliceSpacing[0]=${sliceSpacing[0]%.*}
  sliceSpacing[1]=${sliceSpacing[1]%.*}
  sliceSpacing[2]=${sliceSpacing[2]%.*}



  declare -a zrange
  zrange[0]=${startingx%.*}
  zrange[1]=${endingx%.*}

  zrange[2]=${startingy%.*}
  zrange[3]=${endingy%.*}

  zrange[4]=${startingz%.*}
  zrange[5]=${endingz%.*}


	output_folder=$subject_folder/QC/images/$3
	mkdir -p $output_folder
	sub=$(basename $subject_folder)
	
	if [ "$flag" -eq "1" ]; then
		if [ "$secondOverlayflag" -eq "1" ]; then
			overlay_args="$subject_folder$overlay --name "overlay" $first_overlay_template $subject_folder$secondOverlay --name "overlay1" $second_overlay_template"
		else
			overlay_args="$subject_folder$overlay --name "overlay" $first_overlay_template"

		fi
	fi
        
        if [ "$label_underlay_flag" -q "0" ]; then
		for ((i=0; i<3; i++)); do

			${FSLDIR}/bin/fsleyes render --outfile $output_folder/$sub"_$3_"${axisNames[$i]}.png  --crop 30 --size 6400 2400 --scene lightbox --displaySpace $subject_folder$underlay --zaxis $i --sliceSpacing ${sliceSpacing[$i]} --zrange ${zrange[2*$i]} ${zrange[2*$i+1]} --ncols 6 --nrows 3 --hideCursor --bgColour 0.0 0.0 0.0 --fgColour 1.0 1.0 1.0 --cursorColour 0.0 1.0 0.0 --colourBarLocation top --colourBarLabelSide top-left --colourBarSize 100.0 --labelSize 12 $subject_folder$underlay --name "underlay" --overlayType volume --alpha 100.0 --brightness $brightness_var --contrast $contrast_var --cmap greyscale --negativeCmap greyscale --gamma 0.0 --cmapResolution 256 --interpolation none --numSteps 100 --blendFactor 0.1 --smoothing 0 --resolution 100 --numInnerSteps 10 --clipMode intersection --volume 0 $overlay_args

	

		
		done
        else
			${FSLDIR}/bin/fsleyes render --outfile $output_folder/$sub"_$3_"${axisNames[$i]}.png  --crop 30 --size 6400 2400 --scene lightbox --displaySpace $subject_folder$underlay --zaxis $i --sliceSpacing ${sliceSpacing[$i]} --zrange ${zrange[2*$i]} ${zrange[2*$i+1]} --ncols 6 --nrows 3 --hideCursor --bgColour 0.0 0.0 0.0 --fgColour 1.0 1.0 1.0 --cursorColour 0.0 1.0 0.0 --colourBarLocation top --colourBarLabelSide top-left --colourBarSize 100.0 --labelSize 12 --performance 3 $subject_folder$underlay --name "underlay" --overlayType label --alpha 100.0 --brightness $brightness_var --contrast $contrast_var --lut $underlay_cmap --outlineWidth 1 --volume 0 $overlay_args        
	fi


 

