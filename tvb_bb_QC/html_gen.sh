#!/bin/bash

#USAGE:
#./html_gen.sh $dirSubject $1

subjdir=$1
#"/Users/justinwang/Documents/McIntosh/ukbbqc/full_subs/sub-CC520055"

html_output_dir="/QC/html"

mkdir -p $subjdir$html_output_dir
mkdir -p $subjdir$html_output_dir"/notes"
mkdir -p $subjdir$html_output_dir"/images"
mkdir -p $subjdir$html_output_dir"/css"


cp $BB_BIN_DIR/tvb_bb_QC/resources/sidebartoggles.js $subjdir$html_output_dir
cp $BB_BIN_DIR/tvb_bb_QC/resources/toggles.js $subjdir$html_output_dir
cp $BB_BIN_DIR/tvb_bb_QC/resources/togglesSCFC.js $subjdir$html_output_dir
cp $BB_BIN_DIR/tvb_bb_QC/resources/togglesMELODIC_FIX.js $subjdir$html_output_dir
cp $BB_BIN_DIR/tvb_bb_QC/resources/togglesIDP.js $subjdir$html_output_dir
cp $BB_BIN_DIR/tvb_bb_QC/resources/zoomer.js $subjdir$html_output_dir
cp $BB_BIN_DIR/tvb_bb_QC/resources/notes.txt $subjdir$html_output_dir"/notes"
cp $BB_BIN_DIR/tvb_bb_QC/resources/1.jpg $subjdir$html_output_dir"/images"
cp $BB_BIN_DIR/tvb_bb_QC/resources/missing.png $subjdir$html_output_dir"/images"
cp $BB_BIN_DIR/tvb_bb_QC/resources/missingw.png $subjdir$html_output_dir"/images"
cp $BB_BIN_DIR/tvb_bb_QC/resources/w3.css $subjdir$html_output_dir"/css"

sub=$2
sub_upper=${sub}
#upper later




cat > $subjdir$html_output_dir"/report.html" << EOF

<!DOCTYPE html>
<html lang="en">
<title>QC IMAGE REPORT</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="css/w3.css">
<script src="./zoomer.js" type="text/javascript" charset="utf-8"></script>
<script src="./toggles.js" type="text/javascript" charset="utf-8"></script>
<script src="./sidebartoggles.js" type="text/javascript" charset="utf-8"></script>
<script src="./image_gen_links.js" type="text/javascript" charset="utf-8"></script>

<body class="w3-main" style="background-color:black; " >
<!--document.getElementById('image_link').innerHTML = document.getElementById('ex_a').src;-->


<!-- Header -->
<header class="w3-display-container  w3-center" style="max-height:1000px;">
  <img class="w3-image" src="images/1.jpg" alt="Me" width=100%  style="max-height:1000px;object-fit: cover;">
  
    <div class="w3-display-middle w3-padding-large w3-border w3-wide w3-text-light-grey w3-center" style="background-color:rgba(0, 0, 0, 0.75);">

      <h1 class="w3-hide-medium w3-hide-small w3-xxxlarge">QC IMAGE REPORT</h1>
      <h5 class="w3-hide-large" style="white-space:nowrap">QC IMAGE REPORT</h5>
      
      <h3 class="w3-hide-medium w3-hide-small">$sub_upper</h3>
      <h5 class="w3-hide-medium w3-hide-small">Parcellation - ${PARC_NAME}</h5>
      
    </div>
 

  <!-- Sidebar -->

  <div id="mySidebar" class="sidebar" style="width: 0; margin-left: 0; font-size: 12px">
    <a href="file:notes/" class="w3-center">open notes.txt file in local system to make changes</a>
    <br>
    <iframe src="notes/notes.txt" style="background: #FFFFFF; height: 90%"></iframe>

  </div>

  <!-- Sidebar button -->
   <div id="main" align="left" >
    <button id="togglebutton" class="openbtn sticky" onclick="toggNav()">NOTES</button>  
  </div>




  <!-- Navbar (placed at the bottom of the header image) -->
  <div class="w3-bar w3-light-grey w3-round w3-display-bottommiddle w3-hide-small w3-hide-medium" style="bottom:65px">
    <a href="report.html" class="w3-bar-item w3-button">Home</a>
    <a href="anat.html" class="w3-bar-item w3-button">Anatomical</a>
    <a href="fMRI.html" class="w3-bar-item w3-button">fMRI</a>
    <a href="MELODIC_FIX.html" class="w3-bar-item w3-button">MELODIC-FIX</a>
    <a href="dMRI.html" class="w3-bar-item w3-button">dMRI</a>
    <a href="SCFC.html" class="w3-bar-item w3-button">SC/FC</a>
    <a href="IDP.html" class="w3-bar-item w3-button">IDP</a>
  </div>
</header>

<!-- Navbar on small screens -->
<div class="w3-center w3-black w3-padding-16 w3-hide-large ">
<div class="w3-bar w3-light-grey w3-round ">
  <a href="report.html" class="w3-bar-item w3-button">Home</a>
    <a href="anat.html" class="w3-bar-item w3-button">Anatomical</a>
    <a href="fMRI.html" class="w3-bar-item w3-button">fMRI</a>
    <a href="MELODIC_FIX.html" class="w3-bar-item w3-button">MELODIC-FIX</a>
    <a href="dMRI.html" class="w3-bar-item w3-button">dMRI</a>
    <a href="SCFC.html" class="w3-bar-item w3-button">SC/FC</a>
    <a href="IDP.html" class="w3-bar-item w3-button">IDP</a>
</div>
</div>
<!-- Page content -->
<div class="w3-content w3-padding-large w3-margin-top" id="portfolio" style="color:white; text-align: center;">
<h1>
    <div style="font-size: 20px" > Parcellation: <select name="menu1" id="menu1" onkeydown="IgnoreAlpha(event);">
      <option selected="selected">${PARC_NAME}</option>
      <option id="option_placeholder">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</option>
      <!-- DO NOT REMOVE. PLACEHOLDER FOR SCRIPTS TO INSERT NEW PARC LINKS -->

      
      </select>
      </div>
      <script type="text/javascript">
     var urlmenu = document.getElementById( 'menu1' );
     urlmenu.onchange = function() {
          if (this.options[ this.selectedIndex ].value != ""){
            window.open( this.options[ this.selectedIndex ].value, '_self');
          }
     };
    </script></h1>  
<br>
<br>


<!-- End page content -->
</div>

</body>

<script>

</script>



</html>



EOF




cat > $subjdir$html_output_dir"/anat.html" << EOF

<!DOCTYPE html>
<html lang="en">
<title>ANATOMICAL IMAGE REPORT</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="css/w3.css">
<script src="./zoomer.js" type="text/javascript" charset="utf-8"></script>
<script src="./toggles.js" type="text/javascript" charset="utf-8"></script>
<script src="./sidebartoggles.js" type="text/javascript" charset="utf-8"></script>
<script src="./image_gen_links.js" type="text/javascript" charset="utf-8"></script>

<body class="w3-main" style="background-color:black; " onload="updateImage();updateTitle();update_links();">
<!--document.getElementById('image_link').innerHTML = document.getElementById('ex_a').src;-->


<!-- Header -->
<header class="w3-display-container  w3-center" style="max-height:1000px; ">
  <img class="w3-image" src="images/1.jpg" alt="Me" width=100% style="max-height:1000px;object-fit: cover;">
  
    <div class="w3-display-middle w3-padding-large w3-border w3-wide w3-text-light-grey w3-center" style="background-color:rgba(0, 0, 0, 0.75);">

      <h1 class="w3-hide-medium w3-hide-small w3-xxxlarge">ANATOMICAL IMAGE REPORT</h1>
      <h5 class="w3-hide-large" style="white-space:nowrap">ANATOMICAL IMAGE REPORT</h5>
      
      <h3 class="w3-hide-medium w3-hide-small">$sub_upper</h3>
      <h5 class="w3-hide-medium w3-hide-small">Parcellation - ${PARC_NAME}</h5>
    </div>
 

  <!-- Sidebar -->

  <div id="mySidebar" class="sidebar" style="width: 0; margin-left: 0; font-size: 12px">
    <a href="file:notes/" class="w3-center">open notes.txt file in local system to make changes</a>
    <br>
    <iframe src="notes/notes.txt" style="background: #FFFFFF; height: 90%"></iframe>

  </div>

  <!-- Sidebar button -->
   <div id="main" align="left" >
    <button id="togglebutton" class="openbtn sticky" onclick="toggNav()">NOTES</button>  
  </div>




  <!-- Navbar (placed at the bottom of the header image) -->
  <div class="w3-bar w3-light-grey w3-round w3-display-bottommiddle w3-hide-small w3-hide-medium" style="bottom:65px">
    <a href="report.html" class="w3-bar-item w3-button">Home</a>
    <a href="anat.html" class="w3-bar-item w3-button">Anatomical</a>
    <a href="fMRI.html" class="w3-bar-item w3-button">fMRI</a>
    <a href="MELODIC_FIX.html" class="w3-bar-item w3-button">MELODIC-FIX</a>
    <a href="dMRI.html" class="w3-bar-item w3-button">dMRI</a>
    <a href="SCFC.html" class="w3-bar-item w3-button">SC/FC</a>
    <a href="IDP.html" class="w3-bar-item w3-button">IDP</a>
  </div>
</header>

<!-- Navbar on small screens -->
<div class="w3-center w3-black w3-padding-16 w3-hide-large ">
<div class="w3-bar w3-light-grey w3-round ">
  <a href="report.html" class="w3-bar-item w3-button">Home</a>
    <a href="anat.html" class="w3-bar-item w3-button">Anatomical</a>
    <a href="fMRI.html" class="w3-bar-item w3-button">fMRI</a>
    <a href="MELODIC_FIX.html" class="w3-bar-item w3-button">MELODIC-FIX</a>
    <a href="dMRI.html" class="w3-bar-item w3-button">dMRI</a>
    <a href="SCFC.html" class="w3-bar-item w3-button">SC/FC</a>
    <a href="IDP.html" class="w3-bar-item w3-button">IDP</a>
</div>
</div>
<!-- Page content -->
<div class="w3-content w3-padding-large w3-margin-top" id="portfolio" style="color:white; text-align: center; height: 900px">


  <!-- Images (Portfolio) -->


  <br>______<br><br>
  <h1> $sub_upper 
  <br>
  <div id="analysis_title" style="display: inline; font-size: 28px">EXTRACTION</div><br>    
    <div style="font-size: 20px" > Parcellation: <select name="menu1" id="menu1" onkeydown="IgnoreAlpha(event);">
      <option selected="selected">${PARC_NAME}</option>
      <option id="option_placeholder">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</option>
      <!-- DO NOT REMOVE. PLACEHOLDER FOR SCRIPTS TO INSERT NEW PARC LINKS -->

      
      </select>
      </div>
      <script type="text/javascript">
     var urlmenu = document.getElementById( 'menu1' );
     urlmenu.onchange = function() {
          if (this.options[ this.selectedIndex ].value != ""){
            window.open( this.options[ this.selectedIndex ].value, '_self');
          }
     };
    </script>
    </h1>
  ______<br><br>





<!-------------- OPTIONS -------------->

<!-- Analyses -->
  <label for="Analysis" style="white-space:nowrap;">Analysis <i>(a/d)</i>:
  <select name="Analysis" id="Analysis" onchange="updateTitle();updateImage();update_links();" onkeydown="IgnoreAlpha(event);">
    <optgroup label="T1 Extraction">
      <option value="ex" selected="selected">T1 Extraction</option>
    </optgroup>
    <optgroup label="T1 Registration">
      <option value="re">T1 Registration</option>
    </optgroup>
    <optgroup label="T1 Segmentation">
      <option value="uw">T1 Unlabelled WM</option>
      <option value="ug">T1 Unlabelled GM</option>
      <option value="lc">T1 Labelled GM</option>
      <option value="us">T1 Unlabelled subcort GM</option>
      <option value="ls">T1 Labelled subcort GM</option>
      <option value="vbm">VBM - Parcellation and GM</option>
    </optgroup>
    <optgroup label="T2 FLAIR">
      <option value="Tre">T2 Registration</option>
      <option value="Tbi">T2 BIANCA</option>
    </optgroup>
  </select></label>
  &nbsp&nbsp&nbsp&nbsp
  <!--orientation-->
  <label for="Orientation" id="ori_opts" style="white-space:nowrap;">Orientation <i>(z/x/c)</i>:
  <select name="Orientation" id="Orientation" onchange="updateTitle();updateImage();update_links();" onkeydown="IgnoreAlpha(event);">
    <option value="a">Axial</option>
    <option value="c">Coronal</option>
    <option value="s">Sagittal</option>
  </select></label>
&nbsp&nbsp&nbsp&nbsp


<!--b-value-->
<label for="b-value" id="EDDY_opts"  style="display: none; white-space: nowrap;" >b-value <i>(z/x/c)</i>:
  <select name="b-value" id="b-value" onchange="updateTitle();updateImage();update_links();" onkeydown="IgnoreAlpha(event);">
    <option value="0">0</option>
    <option value="1000">1000</option>
    <option value="2000">2000</option>
  </select></label>
&nbsp&nbsp&nbsp&nbsp

<!-- order appears for registration analyses -->
<div style="display: none; white-space: nowrap;" id="reg_opts"> 
<label id="Order label 1"><input type="radio" id="Order 1" name="Order" value="Order 1" checked="true" onchange="updateTitle();updateImage();update_links();"> Overlay Order 1 <i>(s)</i></label>
&nbsp&nbsp
  <label id="Order label 2"><input type="radio" id="Order 2" name="Order" value="Order 2" onchange="updateTitle();updateImage();update_links();"> Overlay Order 2 <i>(s)</i></label>
</div>

<!-- overlay appears for non-registration analyses -->
  <label id="non_reg_opts" style="white-space:nowrap;"><input id="Overlay check" type="checkbox" checked="true" onchange="updateTitle();updateImage();update_links();"> Toggle Overlay <i>(s)</i></label>
  


  <br>
<br>

Pan enabled for mouse and keyboard <i>(i/j/k/l)</i>

  <br>
<br>



<!---Zoom Canvas--->
<div  id="canvas-container">
  <canvas id='canvas' width='932' height='768' style="border: 1px solid #ccc; "></canvas>
  
  
  <div class="opt" width='932' style="padding-bottom: 80px">
    <ul>
      <li onclick="view.scale(0.85)">Zoom Out <i>(q)</i></li>
      <li onclick="reDraw()">Reset Zoom <i>(w)</i></li>
      <li onclick="view.scale(1.1765)">Zoom In <i>(e)</i></li>
    </ul>

<div>
<label id="zoom_keep_label" style="white-space:nowrap; "><input id="zoom_keep" type="checkbox"> Maintain Zoom when Switching Analyses <i>(r)</i></label></div>
<br>
<i style=" font-size: 12px">
NOTE: Image sizes and therefore maintaining zooms between different analyses can be inconsistent.<br>Some analyses may appear empty when switching into them with a large magnification. Reset Zoom as needed.</i>


    </div>
</div>


<!-------------- UNDERLAYS -------------->
  <!-- UNMASKED UNDERLAY -->
  
  <img src="../images/T1_extraction_unmasked/${sub}_T1_extraction_unmasked_axial.png" id="under_a" style="display: none">
  <img src="../images/T1_extraction_unmasked/${sub}_T1_extraction_unmasked_coronal.png" id="under_c" style="display: none">
  <img src="../images/T1_extraction_unmasked/${sub}_T1_extraction_unmasked_sagittal.png" id="under_s" style="display: none">


  <img src="../images/T1_segmentation_unlabelled_subcort_GM/${sub}_VBM_parcel_unmasked_axial.png" id="under_vbm_a" style="display: none">
  <img src="../images/T1_segmentation_unlabelled_subcort_GM/${sub}_VBM_parcel_unmasked_coronal.png" id="under_vbm_c" style="display: none">
  <img src="../images/T1_segmentation_unlabelled_subcort_GM/${sub}_VBM_parcel_unmasked_sagittal.png" id="under_vbm_s" style="display: none">

  <!-- UNMASKED UNDERLAY SUBCORT -->

  <img src="../images/T1_segmentation_unmasked_subcort/${sub}_T1_segmentation_unmasked_subcort_axial_appended.png" id="under_sub_a" style="display: none">
  <img src="../images/T1_segmentation_unmasked_subcort/${sub}_T1_segmentation_unmasked_subcort_coronal_appended.png" id="under_sub_c" style="display: none">
  <img src="../images/T1_segmentation_unmasked_subcort/${sub}_T1_segmentation_unmasked_subcort_sagittal_appended.png" id="under_sub_s" style="display: none">


  <img src="../images/T2_FLAIR_BIANCA_unmasked/${sub}_T2_FLAIR_BIANCA_unmasked_axial.png" id="under_T2_a" style="display: none">
  <img src="../images/T2_FLAIR_BIANCA_unmasked/${sub}_T2_FLAIR_BIANCA_unmasked_coronal.png" id="under_T2_c" style="display: none">
  <img src="../images/T2_FLAIR_BIANCA_unmasked/${sub}_T2_FLAIR_BIANCA_unmasked_sagittal.png" id="under_T2_s" style="display: none">



<!-------------- OVERLAYS -------------->

  
  <img src="../images/T1_extraction_masked/${sub}_T1_extraction_masked_axial.png" id="ex_a" style="display: none">
  <img src="../images/T1_extraction_masked/${sub}_T1_extraction_masked_coronal.png" id="ex_c" style="display: none">
  <img src="../images/T1_extraction_masked/${sub}_T1_extraction_masked_sagittal.png" id="ex_s" style="display: none">

  
  <img src="../images/T1_registration/order1_${sub}_T1_registration_axial_appended.png" id="o1_a" style="display: none">
  <img src="../images/T1_registration/order1_${sub}_T1_registration_coronal_appended.png" id="o1_c" style="display: none">
  <img src="../images/T1_registration/order1_${sub}_T1_registration_sagittal_appended.png" id="o1_s" style="display: none">
  

  <img src="../images/T1_registration/order2_${sub}_T1_registration_axial_appended.png" id="o2_a" style="display: none">
  <img src="../images/T1_registration/order2_${sub}_T1_registration_coronal_appended.png" id="o2_c" style="display: none">
  <img src="../images/T1_registration/order2_${sub}_T1_registration_sagittal_appended.png" id="o2_s" style="display: none">


  <img src="../images/T1_segmentation_unlabelled_subcort_GM/${sub}_T1_segmentation_unlabelled_subcort_GM_axial_appended.png" id="us_a" style="display: none">
  <img src="../images/T1_segmentation_unlabelled_subcort_GM/${sub}_T1_segmentation_unlabelled_subcort_GM_coronal_appended.png" id="us_c" style="display: none">
  <img src="../images/T1_segmentation_unlabelled_subcort_GM/${sub}_T1_segmentation_unlabelled_subcort_GM_sagittal_appended.png" id="us_s" style="display: none">

  <img src="../images/T1_segmentation_unlabelled_subcort_GM/${sub}_VBM_parcel_GM_overlay_axial.png" id="vbm_a" style="display: none">
  <img src="../images/T1_segmentation_unlabelled_subcort_GM/${sub}_VBM_parcel_GM_overlay_coronal.png" id="vbm_c" style="display: none">
  <img src="../images/T1_segmentation_unlabelled_subcort_GM/${sub}_VBM_parcel_GM_overlay_sagittal.png" id="vbm_s" style="display: none">

  <img src="../images/T1_segmentation_labelled_subcort_GM/${sub}_T1_segmentation_labelled_subcort_GM_axial_appended.png" id="ls_a" style="display: none">
  <img src="../images/T1_segmentation_labelled_subcort_GM/${sub}_T1_segmentation_labelled_subcort_GM_coronal_appended.png" id="ls_c" style="display: none">
  <img src="../images/T1_segmentation_labelled_subcort_GM/${sub}_T1_segmentation_labelled_subcort_GM_sagittal_appended.png" id="ls_s" style="display: none">


  <img src="../images/T1_segmentation_unlabelled_WM/${sub}_T1_segmentation_unlabelled_WM_axial.png" id="uw_a" style="display: none">
  <img src="../images/T1_segmentation_unlabelled_WM/${sub}_T1_segmentation_unlabelled_WM_coronal.png" id="uw_c" style="display: none">
  <img src="../images/T1_segmentation_unlabelled_WM/${sub}_T1_segmentation_unlabelled_WM_sagittal.png" id="uw_s" style="display: none">


  <img src="../images/T1_segmentation_unlabelled_GM/${sub}_T1_segmentation_unlabelled_GM_axial.png" id="ug_a" style="display: none">
  <img src="../images/T1_segmentation_unlabelled_GM/${sub}_T1_segmentation_unlabelled_GM_coronal.png" id="ug_c" style="display: none">
  <img src="../images/T1_segmentation_unlabelled_GM/${sub}_T1_segmentation_unlabelled_GM_sagittal.png" id="ug_s" style="display: none">


  <img src="../images/T1_segmentation_labelled_cortex/${sub}_T1_segmentation_labelled_cortex_axial.png" id="lc_a" style="display: none">
  <img src="../images/T1_segmentation_labelled_cortex/${sub}_T1_segmentation_labelled_cortex_coronal.png" id="lc_c" style="display: none">
  <img src="../images/T1_segmentation_labelled_cortex/${sub}_T1_segmentation_labelled_cortex_sagittal.png" id="lc_s" style="display: none">

  <img src="../images/T2_registration/order1_${sub}_T2_registration_axial_appended.png" id="Tre1_a" style="display: none">
  <img src="../images/T2_registration/order1_${sub}_T2_registration_coronal_appended.png" id="Tre1_c" style="display: none">
  <img src="../images/T2_registration/order1_${sub}_T2_registration_sagittal_appended.png" id="Tre1_s" style="display: none">

  <img src="../images/T2_registration/order2_${sub}_T2_registration_axial_appended.png" id="Tre2_a" style="display: none">
  <img src="../images/T2_registration/order2_${sub}_T2_registration_coronal_appended.png" id="Tre2_c" style="display: none">
  <img src="../images/T2_registration/order2_${sub}_T2_registration_sagittal_appended.png" id="Tre2_s" style="display: none">

  <img src="../images/T2_FLAIR_BIANCA_masked/${sub}_T2_FLAIR_BIANCA_masked_axial.png" id="Tbi_a" style="display: none">
  <img src="../images/T2_FLAIR_BIANCA_masked/${sub}_T2_FLAIR_BIANCA_masked_coronal.png" id="Tbi_c" style="display: none">
  <img src="../images/T2_FLAIR_BIANCA_masked/${sub}_T2_FLAIR_BIANCA_masked_sagittal.png" id="Tbi_s" style="display: none">


<br><br><br><br>________<br><br><br>
<div style="text-align: left; font-size: 12px">
IMAGE FILE:<br> <a id="image_link" href="../images/T1_extraction_masked/${sub}_T1_extraction_masked_axial.png">N/A</a>
<br><br>
UNDERLAY FILE:<br> <a id="underlay" href="">N/A</a>
<br><br>
OVERLAY FILE:<br> <a id="overlay1" href="">N/A</a>
<br><br>
SECOND OVERLAY FILE:<br> <a id="overlay2" href="">N/A</a>
<br><br><br>
</div>
<!-- End page content -->
</div>

</body>

<script>

</script>



</html>



EOF




cat > $subjdir$html_output_dir"/dMRI.html" << EOF

<!DOCTYPE html>
<html lang="en">
<title>dMRI IMAGE REPORT</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="css/w3.css">
<script src="./zoomer.js" type="text/javascript" charset="utf-8"></script>
<script src="./toggles.js" type="text/javascript" charset="utf-8"></script>
<script src="./sidebartoggles.js" type="text/javascript" charset="utf-8"></script>
<script src="./image_gen_links.js" type="text/javascript" charset="utf-8"></script>

<body class="w3-main" style="background-color:black; " onload="updateTitle();updateImage();update_links();">
<!--document.getElementById('image_link').innerHTML = document.getElementById('ex_a').src;-->


<!-- Header -->
<header class="w3-display-container  w3-center" style="max-height:1000px; ">
  <img class="w3-image" src="images/1.jpg" alt="Me" width=100% style="max-height:1000px;object-fit: cover;">
  
    <div class="w3-display-middle w3-padding-large w3-border w3-wide w3-text-light-grey w3-center" style="background-color:rgba(0, 0, 0, 0.75);">

      <h1 class="w3-hide-medium w3-hide-small w3-xxxlarge">dMRI IMAGE REPORT</h1>
      <h5 class="w3-hide-large" style="white-space:nowrap">dMRI IMAGE REPORT</h5>
      
      <h3 class="w3-hide-medium w3-hide-small">$sub_upper</h3>
      <h5 class="w3-hide-medium w3-hide-small">Parcellation - ${PARC_NAME}</h5>
      
    </div>
 

  <!-- Sidebar -->

  <div id="mySidebar" class="sidebar" style="width: 0; margin-left: 0; font-size: 12px">
    <a href="file:notes/" class="w3-center">open notes.txt file in local system to make changes</a>
    <br>
    <iframe src="notes/notes.txt" style="background: #FFFFFF; height: 90%"></iframe>

  </div>

  <!-- Sidebar button -->
   <div id="main" align="left" >
    <button id="togglebutton" class="openbtn sticky" onclick="toggNav()">NOTES</button>  
  </div>




  <!-- Navbar (placed at the bottom of the header image) -->
  <div class="w3-bar w3-light-grey w3-round w3-display-bottommiddle w3-hide-small w3-hide-medium" style="bottom:65px">
    <a href="report.html" class="w3-bar-item w3-button">Home</a>
    <a href="anat.html" class="w3-bar-item w3-button">Anatomical</a>
    <a href="fMRI.html" class="w3-bar-item w3-button">fMRI</a>
    <a href="MELODIC_FIX.html" class="w3-bar-item w3-button">MELODIC-FIX</a>
    <a href="dMRI.html" class="w3-bar-item w3-button">dMRI</a>
    <a href="SCFC.html" class="w3-bar-item w3-button">SC/FC</a>
    <a href="IDP.html" class="w3-bar-item w3-button">IDP</a>
  </div>
</header>

<!-- Navbar on small screens -->
<div class="w3-center w3-black w3-padding-16 w3-hide-large ">
<div class="w3-bar w3-light-grey w3-round ">
  <a href="report.html" class="w3-bar-item w3-button">Home</a>
    <a href="anat.html" class="w3-bar-item w3-button">Anatomical</a>
    <a href="fMRI.html" class="w3-bar-item w3-button">fMRI</a>
    <a href="MELODIC_FIX.html" class="w3-bar-item w3-button">MELODIC-FIX</a>
    <a href="dMRI.html" class="w3-bar-item w3-button">dMRI</a>
    <a href="SCFC.html" class="w3-bar-item w3-button">SC/FC</a>
    <a href="IDP.html" class="w3-bar-item w3-button">IDP</a>
</div>
</div>


<!-- Page content -->
<div class="w3-content w3-padding-large w3-margin-top" id="portfolio" style="color:white; text-align: center; height: 900px">


  <!-- Images (Portfolio) -->


  <br>______<br><br>
  <h1> $sub_upper dMRI 
  <br>
  <div id="analysis_title" style="display: inline; font-size: 28px">DW</div><br>    
    <div style="font-size: 20px" > Parcellation: <select name="menu1" id="menu1" onkeydown="IgnoreAlpha(event);">
      <option selected="selected">${PARC_NAME}</option>
      <option id="option_placeholder">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</option>
      <!-- DO NOT REMOVE. PLACEHOLDER FOR SCRIPTS TO INSERT NEW PARC LINKS -->

      
      </select>
      </div>
      <script type="text/javascript">
     var urlmenu = document.getElementById( 'menu1' );
     urlmenu.onchange = function() {
          if (this.options[ this.selectedIndex ].value != ""){
            window.open( this.options[ this.selectedIndex ].value, '_self');
          }
     };
    </script>
    </h1>
  ______<br><br>





<!-------------- OPTIONS -------------->

<!-- Analyses -->
  <label for="Analysis" style="white-space:nowrap;">Analysis <i>(a/d)</i>:
  <select name="Analysis" id="Analysis" onchange="updateTitle();updateImage();update_links();console.log(this.value)" onkeydown="IgnoreAlpha(event);">
    <optgroup label="EDDY QUAD">
      
      <option value="dw" selected="selected">DW</option>
      <option value="cnr">tSNR/CNR</option>
      <option value="../eddyQUAD/data.qc/qc.pdf">EDDY QUAD Report (opens in new tab)</option>
    </optgroup>
    <optgroup label="EDDY SQUAD">
      <option value="../../../EDDY_SQUAD/group_qc.pdf">EDDY SQUAD Report (opens in new tab)</option>
    </optgroup>
    <optgroup label="Extraction">
      <option value="dex" >Extraction</option>
    </optgroup>
    <optgroup label="Orientation">
      <option value="dorf">Orientation</option>
    </optgroup>
    <optgroup label="Registration">
      <option value="dre">Registration</option>
    </optgroup>
    <optgroup label="Warping">
      <option value="wa">Warping</option>
    </optgroup>
    <optgroup label="Tractography">
      <option value="dxc">Exclude</option>
      <option value="dfs">Light-blue Seeds</option>
      <option value="dfsrb">Random-big Seeds</option>
      <option value="dxs">Exclude with seeds</option>
    </optgroup>
  </select></label>
  &nbsp&nbsp&nbsp&nbsp


  <!--orientation-->
  <label for="Orientation" id="ori_opts" style="white-space:nowrap;">Orientation <i>(z/x/c)</i>:
  <select name="Orientation" id="Orientation" onchange="updateTitle();updateImage();update_links();" onkeydown="IgnoreAlpha(event);">
    <option value="a">Axial</option>
    <option value="c">Coronal</option>
    <option value="s">Sagittal</option>
  </select></label>
&nbsp&nbsp&nbsp&nbsp

<!--b-value-->
<label for="b-value" id="EDDY_opts"  style="display: none;white-space:nowrap;">b-value <i>(z/x/c)</i>:
  <select name="b-value" id="b-value" onchange="updateTitle();updateImage();update_links();" onkeydown="IgnoreAlpha(event);">
    <option value="0">0</option>
    <option value="1000">1000</option>
    <option value="2000">2000</option>
  </select></label>
&nbsp&nbsp&nbsp&nbsp


<!-- order appears for registration analyses -->
<div style="display: none;white-space:nowrap;" id="reg_opts">
<label id="Order label 1"><input type="radio" id="Order 1" name="Order" value="Order 1" checked="true" onchange="updateTitle();updateImage();update_links();"> Overlay Order 1 <i>(s)</i></label>
&nbsp&nbsp
  <label id="Order label 2"><input type="radio" id="Order 2" name="Order" value="Order 2" onchange="updateTitle();updateImage();update_links();"> Overlay Order 2 <i>(s)</i></label>
</div>

<!-- overlay appears for non-registration analyses -->
  <label id="non_reg_opts" style="white-space:nowrap;"><input id="Overlay check" type="checkbox" checked="true" onchange="updateTitle();updateImage();update_links();"> Toggle Overlay <i>(s)</i></label>
  

  <br>
<br>

Pan enabled for mouse and keyboard <i>(i/j/k/l)</i>

  <br>
<br>

<!---Zoom Canvas--->
<div  id="canvas-container">
  <canvas id='canvas' width='932' height='768' style="border: 1px solid #ccc; "></canvas>
  
  
  <div class="opt" width='932' style="padding-bottom: 80px">
    <ul>
      <li onclick="view.scale(0.8)">Zoom Out <i>(q)</i></li>
      <li onclick="reDraw()">Reset Zoom <i>(w)</i></li>
      <li onclick="view.scale(1.20)">Zoom In <i>(e)</i></li>
    </ul>
<div>
<label id="zoom_keep_label" style="white-space:nowrap; "><input id="zoom_keep" type="checkbox"> Maintain Zoom when Switching Analyses <i>(r)</i></label></div><br>
<i style=" font-size: 12px">
NOTE: Image sizes and therefore maintaining zooms between different analyses can be inconsistent.<br>Some analyses may appear empty when switching into them with a large magnification. Reset Zoom as needed.</i>

    </div>


</div>

      

<!-------------- UNDERLAYS -------------->
  <!-- UNMASKED UNDERLAY -->
  

  <img src="../images/dMRI_extraction_unmasked/${sub}_dMRI_extraction_unmasked_axial.png"  id="under_a" style="display: none">
  <img src="../images/dMRI_extraction_unmasked/${sub}_dMRI_extraction_unmasked_coronal.png" id="under_c" style="display: none">
  <img src="../images/dMRI_extraction_unmasked/${sub}_dMRI_extraction_unmasked_sagittal.png" id="under_s" style="display: none">


  <!-- UNMASKED UNDERLAY TRACT -->


  <img src="../images/dMRI_tractography_FA/${sub}_dMRI_tractography_FA_axial.png" id="under_sub_a" style="display: none">
  <img src="../images/dMRI_tractography_FA/${sub}_dMRI_tractography_FA_coronal.png" id="under_sub_c" style="display: none">
  <img src="../images/dMRI_tractography_FA/${sub}_dMRI_tractography_FA_sagittal.png" id="under_sub_s" style="display: none">

  <!-- UNMASKED FA UNDERLAY ORIENTATION -->
  <img src="../images/dMRI_orientation_range_FA/${sub}_dMRI_orientation_range_FA_axial_appended.png" id="under_dorf_a" style="display: none">
  <img src="../images/dMRI_orientation_range_FA/${sub}_dMRI_orientation_range_FA_coronal_appended.png" id="under_dorf_c" style="display: none">
  <img src="../images/dMRI_orientation_range_FA/${sub}_dMRI_orientation_range_FA_sagittal_appended.png" id="under_dorf_s" style="display: none">


<!-------------- OVERLAYS -------------->

  <img src="../eddyQUAD/data.qc/avg_b0.png" id="dw_0" style="display: none">
  <img src="../eddyQUAD/data.qc/avg_b1000.png" id="dw_1000" style="display: none">
  <img src="../eddyQUAD/data.qc/avg_b2000.png" id="dw_2000" style="display: none">
  <img src="../eddyQUAD/data.qc/cnr0000.nii.gz.png" id="cnr_0" style="display: none">
  <img src="../eddyQUAD/data.qc/cnr0001.nii.gz.png" id="cnr_1000" style="display: none">
  <img src="../eddyQUAD/data.qc/cnr0002.nii.gz.png" id="cnr_2000" style="display: none">

  <img src="../images/dMRI_extraction_masked/${sub}_dMRI_extraction_masked_axial.png" id="dex_a" style="display: none">
  <img src="../images/dMRI_extraction_masked/${sub}_dMRI_extraction_masked_coronal.png" id="dex_c" style="display: none">
  <img src="../images/dMRI_extraction_masked/${sub}_dMRI_extraction_masked_sagittal.png" id="dex_s" style="display: none">
  


  <img src="../images/dMRI_orientation_with_FA/${sub}_dMRI_orientation_with_FA_axial_appended.png" id="dorf_a" style="display: none">
  <img src="../images/dMRI_orientation_with_FA/${sub}_dMRI_orientation_with_FA_coronal_appended.png" id="dorf_c" style="display: none">
  <img src="../images/dMRI_orientation_with_FA/${sub}_dMRI_orientation_with_FA_sagittal_appended.png" id="dorf_s" style="display: none">




  <img src="../images/dMRI_registration/order1_${sub}_dMRI_registration_axial_appended.png" id="o1_a" style="display: none">
  <img src="../images/dMRI_registration/order1_${sub}_dMRI_registration_coronal_appended.png" id="o1_c" style="display: none">
  <img src="../images/dMRI_registration/order1_${sub}_dMRI_registration_sagittal_appended.png" id="o1_s" style="display: none">

  <img src="../images/dMRI_registration/order2_${sub}_dMRI_registration_axial_appended.png" id="o2_a" style="display: none">
  <img src="../images/dMRI_registration/order2_${sub}_dMRI_registration_coronal_appended.png" id="o2_c" style="display: none">
  <img src="../images/dMRI_registration/order2_${sub}_dMRI_registration_sagittal_appended.png" id="o2_s" style="display: none">


  <img src="../images/DWI_warping/order1_${sub}_DWI_warping_axial_appended.png" id="wa1_a" style="display: none">
  <img src="../images/DWI_warping/order1_${sub}_DWI_warping_coronal_appended.png" id="wa1_c" style="display: none">
  <img src="../images/DWI_warping/order1_${sub}_DWI_warping_sagittal_appended.png" id="wa1_s" style="display: none">

  <img src="../images/DWI_warping/order2_${sub}_DWI_warping_axial_appended.png" id="wa2_a" style="display: none">
  <img src="../images/DWI_warping/order2_${sub}_DWI_warping_coronal_appended.png" id="wa2_c" style="display: none">
  <img src="../images/DWI_warping/order2_${sub}_DWI_warping_sagittal_appended.png" id="wa2_s" style="display: none">



  <img src="../images/dMRI_tractography_seeds/${sub}_dMRI_tractography_seeds_axial.png"  id="dfs_a" style="display: none">
  <img src="../images/dMRI_tractography_seeds/${sub}_dMRI_tractography_seeds_coronal.png" id="dfs_c" style="display: none">
  <img src="../images/dMRI_tractography_seeds/${sub}_dMRI_tractography_seeds_sagittal.png" id="dfs_s" style="display: none">

  <img src="../images/dMRI_tractography_seeds_rb/${sub}_dMRI_tractography_seeds_rb_axial.png"  id="dfsrb_a" style="display: none">
  <img src="../images/dMRI_tractography_seeds_rb/${sub}_dMRI_tractography_seeds_rb_coronal.png" id="dfsrb_c" style="display: none">
  <img src="../images/dMRI_tractography_seeds_rb/${sub}_dMRI_tractography_seeds_rb_sagittal.png" id="dfsrb_s" style="display: none">

  <img src="../images/dMRI_tractography_exclude/${sub}_dMRI_tractography_exclude_axial.png" id="dxc_a" style="display: none">
  <img src="../images/dMRI_tractography_exclude/${sub}_dMRI_tractography_exclude_coronal.png" id="dxc_c" style="display: none">
  <img src="../images/dMRI_tractography_exclude/${sub}_dMRI_tractography_exclude_sagittal.png" id="dxc_s" style="display: none">
  

  <img src="../images/dMRI_tractography_exclude_seeds/${sub}_dMRI_tractography_exclude_seeds_axial.png" id="dxs_a" style="display: none">
  <img src="../images/dMRI_tractography_exclude_seeds/${sub}_dMRI_tractography_exclude_seeds_coronal.png" id="dxs_c" style="display: none">
  <img src="../images/dMRI_tractography_exclude_seeds/${sub}_dMRI_tractography_exclude_seeds_sagittal.png" id="dxs_s" style="display: none">


<br><br><br><br>________<br><br><br>
<div style="text-align: left; font-size: 12px" >
IMAGE FILE:<br> <a id="image_link" href="../images/T1_extraction_masked/${sub}_T1_extraction_masked_axial.png">N/A</a>
<br><br>
UNDERLAY FILE:<br> <a id="underlay" href="">N/A</a>
<br><br>
OVERLAY FILE:<br> <a id="overlay1" href="">N/A</a>
<br><br>
SECOND OVERLAY FILE:<br> <a id="overlay2" href="">N/A</a>
<br><br><br>
</div>
<!-- End page content -->
</div>

</body>

<script>

</script>



</html>



EOF




farray=()
while IFS=  read -r -d $'\0'; do
    farray+=("$REPLY")
done < <(find $subjdir/fMRI -maxdepth 1 -type d -name "*.feat" -print0)




array=()
while IFS=  read -r -d $'\0'; do
    array+=("$REPLY")
done < <(find $subjdir/fMRI -maxdepth 1 -type d -name "*.ica" -print0)
IFS=$'\n' array=($(sort <<<"${array[*]}")); unset IFS







cat > $subjdir$html_output_dir"/fMRI.html" << EOF

<!DOCTYPE html>
<html lang="en">
<title>fMRI IMAGE REPORT</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="css/w3.css">
<script src="./sidebartoggles.js" type="text/javascript" charset="utf-8"></script>

<body class="w3-main" style="background-color:black; " onload="updateTitle();updateImage();updateTitle();">
<!--document.getElementById('image_link').innerHTML = document.getElementById('ex_a').src;-->


<!-- Header -->
<header class="w3-display-container  w3-center" style="max-height:1000px; ">
  <img class="w3-image" src="images/1.jpg" alt="Me" width=100% style="max-height:1000px;object-fit: cover;">
  
    <div class="w3-display-middle w3-padding-large w3-border w3-wide w3-text-light-grey w3-center" style="background-color:rgba(0, 0, 0, 0.75);">

      <h1 class="w3-hide-medium w3-hide-small w3-xxxlarge">fMRI IMAGE REPORT</h1>
      <h5 class="w3-hide-large" style="white-space:nowrap">fMRI IMAGE REPORT</h5>
      
      <h3 class="w3-hide-medium w3-hide-small">$sub_upper</h3>
      <h5 class="w3-hide-medium w3-hide-small">Parcellation - ${PARC_NAME}</h5>
      
    </div>
 

  <!-- Sidebar -->

  <div id="mySidebar" class="sidebar" style="width: 0; margin-left: 0; font-size: 12px">
    <a href="file:notes/" class="w3-center">open notes.txt file in local system to make changes</a>
    <br>
    <iframe src="notes/notes.txt" style="background: #FFFFFF; height: 90%"></iframe>

  </div>

  <!-- Sidebar button -->
   <div id="main" align="left" >
    <button id="togglebutton" class="openbtn sticky" onclick="toggNav()">NOTES</button>  
  </div>




  <!-- Navbar (placed at the bottom of the header image) -->
  <div class="w3-bar w3-light-grey w3-round w3-display-bottommiddle w3-hide-small w3-hide-medium" style="bottom:65px">
    <a href="report.html" class="w3-bar-item w3-button">Home</a>
    <a href="anat.html" class="w3-bar-item w3-button">Anatomical</a>
    <a href="fMRI.html" class="w3-bar-item w3-button">fMRI</a>
    <a href="MELODIC_FIX.html" class="w3-bar-item w3-button">MELODIC-FIX</a>
    <a href="dMRI.html" class="w3-bar-item w3-button">dMRI</a>
    <a href="SCFC.html" class="w3-bar-item w3-button">SC/FC</a>
    <a href="IDP.html" class="w3-bar-item w3-button">IDP</a>
  </div>
</header>

<!-- Navbar on small screens -->
<div class="w3-center w3-black w3-padding-16 w3-hide-large ">
<div class="w3-bar w3-light-grey w3-round ">
  <a href="report.html" class="w3-bar-item w3-button">Home</a>
    <a href="anat.html" class="w3-bar-item w3-button">Anatomical</a>
    <a href="fMRI.html" class="w3-bar-item w3-button">fMRI</a>
    <a href="MELODIC_FIX.html" class="w3-bar-item w3-button">MELODIC-FIX</a>
    <a href="dMRI.html" class="w3-bar-item w3-button">dMRI</a>
    <a href="SCFC.html" class="w3-bar-item w3-button">SC/FC</a>
    <a href="IDP.html" class="w3-bar-item w3-button">IDP</a>
</div>
</div>


<!-- Page content -->
<div class="w3-content w3-padding-large w3-margin-top" id="portfolio" style="color:white; text-align: center; height: 925px">


  <!-- Images (Portfolio) -->

<br><br><a name="fMRI_REPORTS">______</a><br><br>
  <h1> fMRI REPORTS </h1>

  <h1>
    <div style="font-size: 20px" > Parcellation: <select name="menu1" id="menu1" onkeydown="IgnoreAlpha(event);">
      <option selected="selected">${PARC_NAME}</option>
      <option id="option_placeholder">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</option>
      <!-- DO NOT REMOVE. PLACEHOLDER FOR SCRIPTS TO INSERT NEW PARC LINKS -->

      
      </select>
      </div>
      <script type="text/javascript">
     var urlmenu = document.getElementById( 'menu1' );
     urlmenu.onchange = function() {
          if (this.options[ this.selectedIndex ].value != ""){
            window.open( this.options[ this.selectedIndex ].value, '_self');
          }
     };
    </script></h1>
  ______

EOF


#for each .feat file
for t in ${farray[@]}; do
  tfMRI_dir=`basename $t`
  tfMRI_ver=`basename $t`
  tfMRI_ver=${tfMRI_ver%.*}
cat <<EOF >> $subjdir$html_output_dir"/fMRI.html"

<br><br><br>
  <h3> <a href="../../fMRI/$tfMRI_dir/report.html">$tfMRI_ver REPORT</a> </h3><a href="../../fMRI/$tfMRI_dir/report_unwarp.html">$tfMRI_ver Field Map Report</a><br>
 

     <br>

EOF
done




#for each .ica file
for t in ${array[@]}; do
  rfMRI_dir=`basename $t`
  rfMRI_ver=`basename $t`
  rfMRI_ver=${rfMRI_ver%.*}
cat <<EOF >> $subjdir$html_output_dir"/fMRI.html"

<br><br><br>
  <h3> <a href="../../fMRI/$rfMRI_dir/report.html">$rfMRI_ver REPORT</a> </h3><a href="../../fMRI/$rfMRI_dir/report_unwarp.html">$rfMRI_ver Field Map Report</a><br>
 

     <br>

EOF
done


cat <<EOF >> $subjdir$html_output_dir"/fMRI.html"

<!-- End page content -->
</div>

</body>

<script>
 updateTitle();updateImage();
</script>



</html>



EOF




cat > $subjdir$html_output_dir"/SCFC.html" << EOF

<!DOCTYPE html>
<html lang="en">
<title>SC/FC IMAGE REPORT</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="css/w3.css">
<script src="./togglesSCFC.js" type="text/javascript" charset="utf-8"></script>
<script src="./sidebartoggles.js" type="text/javascript" charset="utf-8"></script>

<body class="w3-main" style="background-color:black; " onload="updateTitle();updateImage();updateTitle();">
<!--document.getElementById('image_link').innerHTML = document.getElementById('ex_a').src;-->


<!-- Header -->
<header class="w3-display-container  w3-center" style="max-height:1000px; ">
  <img class="w3-image" src="images/1.jpg" alt="Me" width=100% style="max-height:1000px;object-fit: cover;">
   
    <div class="w3-display-middle w3-padding-large w3-border w3-wide w3-text-light-grey w3-center" style="background-color:rgba(0, 0, 0, 0.75);">

      <h1 class="w3-hide-medium w3-hide-small w3-xxxlarge">SC/FC IMAGE REPORT</h1>
      <h5 class="w3-hide-large" style="white-space:nowrap">SC/FC IMAGE REPORT</h5>
      
      <h3 class="w3-hide-medium w3-hide-small">$sub_upper</h3>
      <h5 class="w3-hide-medium w3-hide-small">Parcellation - ${PARC_NAME}</h5>
      
    </div>
 

  <!-- Sidebar -->

  <div id="mySidebar" class="sidebar" style="width: 0; margin-left: 0; font-size: 12px">
    <a href="file:notes/" class="w3-center">open notes.txt file in local system to make changes</a>
    <br>
    <iframe src="notes/notes.txt" style="background: #FFFFFF; height: 90%"></iframe>

  </div>

  <!-- Sidebar button -->
   <div id="main" align="left" >
    <button id="togglebutton" class="openbtn sticky" onclick="toggNav()">NOTES</button>  
  </div>




  <!-- Navbar (placed at the bottom of the header image) -->
  <div class="w3-bar w3-light-grey w3-round w3-display-bottommiddle w3-hide-small w3-hide-medium" style="bottom:65px">
    <a href="report.html" class="w3-bar-item w3-button">Home</a>
    <a href="anat.html" class="w3-bar-item w3-button">Anatomical</a>
    <a href="fMRI.html" class="w3-bar-item w3-button">fMRI</a>
    <a href="MELODIC_FIX.html" class="w3-bar-item w3-button">MELODIC-FIX</a>
    <a href="dMRI.html" class="w3-bar-item w3-button">dMRI</a>
    <a href="SCFC.html" class="w3-bar-item w3-button">SC/FC</a>
    <a href="IDP.html" class="w3-bar-item w3-button">IDP</a>
  </div>
</header>

<!-- Navbar on small screens -->
<div class="w3-center w3-black w3-padding-16 w3-hide-large ">
<div class="w3-bar w3-light-grey w3-round ">
  <a href="report.html" class="w3-bar-item w3-button">Home</a>
    <a href="anat.html" class="w3-bar-item w3-button">Anatomical</a>
    <a href="fMRI.html" class="w3-bar-item w3-button">fMRI</a>
    <a href="MELODIC_FIX.html" class="w3-bar-item w3-button">MELODIC-FIX</a>
    <a href="dMRI.html" class="w3-bar-item w3-button">dMRI</a>
    <a href="SCFC.html" class="w3-bar-item w3-button">SC/FC</a>
    <a href="IDP.html" class="w3-bar-item w3-button">IDP</a>
</div>
</div>


<!-- Page content -->
<div class="w3-content w3-padding-large w3-margin-top" id="portfolio" style="color:white; text-align: center; height: 900px">


  <!-- Images (Portfolio) -->


  <br>______<br><br>
  <h1> $sub_upper SC/FC 
  <br>
  <div id="analysis_title" style="display: inline; font-size: 28px">STRUCTURAL CONNECTIVITY</div><br>    
    <div style="font-size: 20px" > Parcellation: <select name="menu1" id="menu1" onkeydown="IgnoreAlpha(event);">
      <option selected="selected">${PARC_NAME}</option>
      <option id="option_placeholder">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</option>
      <!-- DO NOT REMOVE. PLACEHOLDER FOR SCRIPTS TO INSERT NEW PARC LINKS -->

      
      </select>
      </div>
      <script type="text/javascript">
     var urlmenu = document.getElementById( 'menu1' );
     urlmenu.onchange = function() {
          if (this.options[ this.selectedIndex ].value != ""){
            window.open( this.options[ this.selectedIndex ].value, '_self');
          }
     };
    </script>
    </h1>
  ______<br><br>





<!-------------- OPTIONS -------------->

<!-- Analyses -->
  <label for="Analysis" style="white-space:nowrap;">Analysis <i>(a/d)</i>:
  <select name="Analysis" id="Analysis" onchange="updateTitle();updateImage();" onkeydown="IgnoreAlpha(event);">

    <optgroup label="Structural Connectivity">
      <option value="group_sc" id="sc" selected="selected">Structural Connectivity</option>
    </optgroup>
    <optgroup label="Tract Length">
      <option value="group_tl" id="tl">Tract Length</option>
    </optgroup>


EOF


#for each .feat file
# for t in ${farray[@]}; do
#   tfMRI_ver=`basename $t`
#   tfMRI_ver=${tfMRI_ver%.*}
# cat <<EOF >> $subjdir$html_output_dir"/SCFC.html"

#     <optgroup label="$tfMRI_ver">
#       <option value="group_$tfMRI_ver" id="$tfMRI_ver">$tfMRI_ver Graphs</option>
#     </optgroup>

# EOF
# done




#for each .ica file
for t in ${array[@]}; do
  rfMRI_ver=`basename $t`
  rfMRI_ver=${rfMRI_ver%.*}
cat <<EOF >> $subjdir$html_output_dir"/SCFC.html"

    <optgroup label="$rfMRI_ver">
      <option value="group_f$rfMRI_ver" id="f$rfMRI_ver">$rfMRI_ver Functional Connectivity</option>
      <option value="group_r$rfMRI_ver" id="r$rfMRI_ver">$rfMRI_ver ROI Carpet Plot & Displacement Graph</option>
    </optgroup>

EOF
done


cat <<EOF >> $subjdir$html_output_dir"/SCFC.html"

  </select></label>
  &nbsp&nbsp&nbsp&nbsp




<!-------------- OVERLAYS -------------->


  <br> <br> 

<div class="group_sc" style="display: none;">

<img src="../SC_FC/${sub}_SC.png" class="sc" width="1000" >
<br><br>
<img src="../SC_FC/${sub}_SC_hist.png" class="sc" width="1000" >
</div>


<div class="group_tl" style="display: none;">

<img src="../SC_FC/${sub}_TL.png" class="tl" width="1000" >
<br><br>
<img src="../SC_FC/${sub}_TL_hist.png" class="tl" width="1000" >
</div>

EOF


#for each .feat file
# for t in ${farray[@]}; do
#   tfMRI_dir=`basename $t`
#   tfMRI_ver=`basename $t`
#   tfMRI_ver=${tfMRI_ver%.*}

# cat <<EOF >> $subjdir$html_output_dir"/SCFC.html"

#   <div class="group_$tfMRI_ver" style="display: none;">
#       <a href="../../fMRI/$tfMRI_dir/report_prestats.html">tfMRI SC FC</a>
#       <br>
#       <img src="../../fMRI/$tfMRI_dir/mc/disp.png" class="$tfMRI_ver" style="width:100%" >
#       <img src="../../fMRI/$tfMRI_dir/mc/rot.png" class="$tfMRI_ver" style="width:100%" >
#       <img src="../../fMRI/$tfMRI_dir/mc/trans.png" class="$tfMRI_ver" style="width:100%" >

# </div>
# EOF
# done





#for each .ica file
for t in ${array[@]}; do
  rfMRI_dir=`basename $t`
  rfMRI_ver=`basename $t`
  rfMRI_ver=${rfMRI_ver%.*}

cat <<EOF >> $subjdir$html_output_dir"/SCFC.html"



<div class="group_f$rfMRI_ver" style="display: none;">
  <img src="../SC_FC/${sub}_${rfMRI_ver}_ica_FC.png"  class="f$rfMRI_ver" width="1000"  style="">
  <br><br>
    <img src="../SC_FC/${sub}_${rfMRI_ver}_ica_FC_hist.png"  class="f$rfMRI_ver" width="1000"  style="">
</div>


<div class="group_r$rfMRI_ver" style="display: none;; ">
    <div style="color:black; text-align: center; background-color: white">
  <img src="../SC_FC/${sub}_${rfMRI_ver}_ica_carpet.png"  class="r$rfMRI_ver" width="1000"  style="float: left; width:90%;">
  <br>
  <img src="../../fMRI/$rfMRI_dir/mc/disp.png"  class="r$rfMRI_ver" style="float: left;padding-left: 39px; width:97.5%" />
  <img src="../../fMRI/$rfMRI_dir/mc/rot.png"  class="r$rfMRI_ver" style="float: left;padding-left: 15px;  width:92.5%" />
  <img src="../../fMRI/$rfMRI_dir/mc/trans.png"  class="r$rfMRI_ver" style="padding-right: 38px;  width:94%" />
</div>
</div>




EOF
done

cat <<EOF >> $subjdir$html_output_dir"/SCFC.html"

<div style="text-align: left; font-size: 12px" >
IMAGE 1 FILE:<br> <a id="im1" href="../images/T1_extraction_masked/${sub}_T1_extraction_masked_axial.png">N/A</a>
<br><br>
IMAGE 2 FILE:<br> <a id="im2" href="">N/A</a>
<br><br>
IMAGE 3 FILE:<br> <a id="im3" href="" >N/A</a>
<br><br><br>
</div>
<!-- End page content -->
</div>

</body>

<script>
 updateTitle();updateImage();
</script>



</html>




EOF


$BB_BIN_DIR/tvb_bb_QC/MELODIC_FIX_html_gen.sh $subjdir $sub
