#!/bin/env python
#
# Script name: IDP_html_gen.py
#
# Description: Script to generate IDP page of QC html report.
#
## Author: Justin Wang

import pandas as pd
import numpy as np
import sys
import os



def IDP_html_gen(subj, PARC_NAME):
    """Function that generates the IDP page of the QC report for a
    subject.

    TODO: remove duplicate code by having a single function used
            twice - once for low-priority and once for high
    TODO: handle missing low-priority lines in the IDPoi
    TODO: separate low and high priority IDPs in report

    Parameters
    ----------
    subj : string
        Full path to subject's directory.

    """

    # remove trailing forward slashes in subject paths
    if subj.endswith("/"):
        subj = subj[:-1]

    QC_dir = subj + "/QC/html/"
    IDP_dir = subj + "/IDP_files/"

    # save IDPois to txt files for future reference
    priority_output = pd.read_csv(r"" + IDP_dir + "priority_IDPs.tsv", delimiter="\t")
    non_priority_output = pd.read_csv(
        r"" + IDP_dir + "non_priority_IDPs.tsv", delimiter="\t"
    )
    new_IDP_output = pd.read_csv(r"" + IDP_dir + "tvb_new_IDPs.tsv", delimiter="\t")

    subjname = os.path.basename(subj)

    # write IDP.html with IDP information
    f = open(QC_dir + "IDP.html", "a")

    message = (
        """


    <!DOCTYPE html>
    <html lang="en">
    <title>IDP IMAGE REPORT</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="css/w3.css">

    <script src="./togglesIDP.js" type="text/javascript" charset="utf-8"></script>
    <script src="./sidebartoggles.js" type="text/javascript" charset="utf-8"></script>
    <style>
      th, td {
      padding: 5px;
    }
    </style>
    <body class="w3-main" style="background-color:black; " onload="updateTitle();updateImage();updateTitle();">
    <!--document.getElementById('image_link').innerHTML = document.getElementById('ex_a').src;-->


    <!-- Header -->
    <header class="w3-display-container  w3-center" style="max-height:1000px; ">
      <img class="w3-image" src="images/1.jpg" alt="Me" width=100% style="max-height:1000px;object-fit: cover;">
      
        <div class="w3-display-middle w3-padding-large w3-border w3-wide w3-text-light-grey w3-center" style="background-color:rgba(0, 0, 0, 0.75);">

          <h1 class="w3-hide-medium w3-hide-small w3-xxxlarge">IDP IMAGE REPORT</h1>
          <h5 class="w3-hide-large" style="white-space:nowrap">IDP IMAGE REPORT</h5>
          

          <h3 class="w3-hide-medium w3-hide-small">"""
        + subjname
        + """</h3>
          <h5 class="w3-hide-medium w3-hide-small">Parcellation - """
        + PARC_NAME
        + """</h5>
          
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
    <div class="w3-content w3-padding-large w3-margin-top" id="portfolio" style="color:white; text-align: center; >



	  <!-- Images (Portfolio) -->

	<br><br><a name="fMRI_REPORTS">______</a><br><br>
	  <h1> IDP REPORTS </h1>
      <h1>
    <div style="font-size: 20px" > Parcellation: <select name="menu1" id="menu1" onkeydown="IgnoreAlpha(event);">

      <option selected="selected">"""
        + PARC_NAME
        + """</option>
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
	  ______<br><br><br>

	
        <label for="IDPs" style="white-space:nowrap;">IDPs <i>(q/e)</i>:
  <select name="IDPs" id="IDPs" onchange="updateTitle();updateImage();" onkeydown="IgnoreAlpha(event);">
    


<option value="High-priority IDPs" id="High-priority IDPs">High-priority IDPs</option>
<option value="New TVB IDPs" id="New TVB IDPs">New TVB IDPs</option>


<option value="Low-priority IDPs" id="Low-priority IDPs">Low-priority IDPs</option>

<option value="All IDPs" id="All IDPs">All Significant IDPs</option>


  </select></label>
  &nbsp&nbsp&nbsp&nbsp

<br><br>

    
  <div style="font-size: 10px">
      <table style="  margin-left: auto;
      margin-right: auto; text-align: left;">
        <tr>
          <th>IDP Name (short)</th>
          <th>Category</th>
          <th>Value</th>
          <th>Unit</th>
        </tr>


	"""
    )

    f.write(message)

    # write priority df
    # background-color:darkred or darkgreen depending on value
    for index, row in priority_output.iterrows():
        color = ""
        try:
            if str(row["flag"]) == "True":
                color = "background-color:darkred"

            if str(row["flag"]) == "False":
                color = "background-color:darkgreen"
        except:
            print("Error: no flag column")
        message = (
            """
			<tr style="display: none; """
            + color
            + """" name="High-priority IDPs">

			  <td>"""
            + str(row["short"])
            + """</td>
			  <td>"""
            + str(row["category"])
            + """</td>
			  <td>"""
            + str("{:e}".format(float(row["value"])))
            + """</td>
			  <td>"""
            + str(row["unit"])
            + """</td>
			</tr>
			
			"""
        )
        f.write(message)

    # write new df in the same table
    for index, row in new_IDP_output.iterrows():
        color = ""

        try:
            if row["flag"] == "TRUE":
                color = "darkred"

            if row["flag"] == "FALSE":
                color = "darkgreen"
        except:
            print("Error: no flag column")
        message = (
            """
            <tr style="display: none; """
            + color
            + """" name="New TVB IDPs">
              <td>"""
            + str(row["short"])
            + """</td>
              <td>"""
            + str(row["category"])
            + """</td>
              <td>"""
            + str(row["value"])
            + """</td>
              <td>"""
            + str(row["unit"])
            + """</td>
            </tr>

            """
        )
        f.write(message)

    # write non-priority df in the same table
    for index, row in non_priority_output.iterrows():
        color = ""

        try:
            if row["flag"] == "TRUE":
                color = "darkred"

            if row["flag"] == "FALSE":
                color = "darkgreen"
        except:
            print("Error: no flag column")

        message = (
            """
			<tr style="display: none; """
            + color
            + """" name="Low-priority IDPs">

			  <td>"""
            + str(row["short"])
            + """</td>
			  <td>"""
            + str(row["category"])
            + """</td>
			  <td>"""
            + str("{:e}".format(float(row["value"])))
            + """</td>
			  <td>"""
            + str(row["unit"])
            + """</td>
			</tr>

			"""
        )
        f.write(message)

    message = (
        """ </table>


    <br>

    <br>

    <br>

    <a href="../../IDP_files_"""
        + PARC_NAME
        + """/" id="hi_IDP" class="w3-bar-item w3-button">High-Priority IDPs: """
        + str(IDP_dir)[:-1]
        + "_"
        + PARC_NAME
        + "/priority_IDPs.tsv"
        + """</a>
    <br>

    <a href="../../IDP_files_"""
        + PARC_NAME
        + """/" id="new_IDP" class="w3-bar-item w3-button">New TVB IDPs: """
        + str(IDP_dir)[:-1]
        + "_"
        + PARC_NAME
        + "/tvb_new_IDPs.tsv"
        + """</a>
    <br>

    <a href="../../IDP_files_"""
        + PARC_NAME
        + """/" id="low_IDP" class="w3-bar-item w3-button">Lower-priority IDPs: """
        + str(IDP_dir)[:-1]
        + "_"
        + PARC_NAME
        + "/non_priority_IDPs.tsv"
        + """</a>
    <br>


    <a href="../../IDP_files_"""
        + PARC_NAME
        + """/" id="combo_IDP" class="w3-bar-item w3-button">Combination of the above IDPs: """
        + str(IDP_dir)[:-1]
        + "_"
        + PARC_NAME
        + "/significant_IDPs.tsv"
        + """</a>

        <br>
        <br>
        </div>


	<!-- End page content -->
	</div>

	</body>

	<script>
	updateTitle();updateImage();
    
    document.getElementById("hi_IDP").innerHTML = document.getElementById("hi_IDP").href;
    document.getElementById("hi_IDP").innerHTML = document.getElementById("hi_IDP").innerHTML + "priority_IDPs.tsv"

    document.getElementById("new_IDP").innerHTML = document.getElementById("new_IDP").href;
    document.getElementById("new_IDP").innerHTML = document.getElementById("new_IDP").href + "tvb_new_IDPs.tsv";

    document.getElementById("low_IDP").innerHTML = document.getElementById("low_IDP").href;
    document.getElementById("low_IDP").innerHTML = document.getElementById("low_IDP").href + "non_priority_IDPs.tsv";

    document.getElementById("combo_IDP").innerHTML = document.getElementById("combo_IDP").href;
    document.getElementById("combo_IDP").innerHTML = document.getElementById("combo_IDP").href + "significant_IDPs.tsv";

	</script>



	</html>

	 """
    )

    f.write(message)

    f.close()


if __name__ == "__main__":
    """Generates IDP.html of the QC report using IDP txts.



    Usage
    ----------

    python  IDP_html_gen.py  subj



    Arguments
    ----------
    subj :
        Full path to subject's directory.


    """
    # try:

    IDP_html_gen(sys.argv[1], sys.argv[2])
