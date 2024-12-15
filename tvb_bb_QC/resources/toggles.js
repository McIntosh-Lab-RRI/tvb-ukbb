
  let view
  let canvas


document.addEventListener('keydown', logKey);


function IgnoreAlpha(e) {
  if (!e) {
    e = window.event;
  }
  if (e.keyCode >= 65 && e.keyCode <= 90) // A to Z
  {
    e.returnValue = false;
    e.cancel = true;
  }
}


function logKey(e) {
  if(e.code=="KeyI"){
    view.pan(0,75);
  }
  if(e.code=="KeyK"){
    view.pan(0,-75);
  }
  if(e.code=="KeyJ"){
    view.pan(75,0);
  }
  if(e.code=="KeyL"){
    view.pan(-75,0);
  }
  if(e.code=="KeyQ"){
    view.scale(0.85);
  }
  if(e.code=="KeyW"){
    resetDraw();
  }
  if(e.code=="KeyE"){
    view.scale(1.15);
  }
  if(e.code=="KeyA"){
    var select = document.getElementById('Analysis');
    if(select.selectedIndex==0){
      select.selectedIndex=select.length - 1
    }
    else{
      if (select[select.selectedIndex - 1].value == "../../../EDDY_SQUAD/group_qc.pdf"){
        select.selectedIndex = select.selectedIndex - 3;
      }
      else{
        select.selectedIndex--;
      }

      


    }
    updateTitle();updateImage();update_links();
  }
  if(e.code=="KeyS"){
    var select = document.getElementById('Overlay check');
    
    if (select.checked==true){
      select.checked = false;
    }
    else{
      select.checked = true;
    }

    var select1 = document.getElementById('Order 1');
    var select2 = document.getElementById('Order 2');
    
    if (select1.checked==true){
      select2.checked = true;
    }
    else{
      select1.checked = true;
    }

    updateTitle();updateImage();update_links();
  }


  if(e.code=="KeyD"){
    var select = document.getElementById('Analysis');
    if(select.selectedIndex==select.length - 1){
      select.selectedIndex=0
    }
    else{
      if (select[select.selectedIndex + 1].value == "../eddyQUAD/data.qc/qc.pdf"){
        select.selectedIndex = select.selectedIndex + 3;
      }
      else{
        select.selectedIndex++;
      }
    }
    updateTitle();updateImage();update_links();
  }

  if(e.code=="KeyZ"){
    var select = document.getElementById('Orientation');
    select.selectedIndex="0";

    var select = document.getElementById('b-value');
    select.selectedIndex="0";
    updateTitle();updateImage();update_links();
  }
  if(e.code=="KeyX"){
    var select = document.getElementById('Orientation');
    select.selectedIndex="1";

    var select = document.getElementById('b-value');
    select.selectedIndex="1";
    updateTitle();updateImage();update_links();
  }
  if(e.code=="KeyC"){
    var select = document.getElementById('Orientation');
    select.selectedIndex="2";

    var select = document.getElementById('b-value');
    select.selectedIndex="2";
    updateTitle();updateImage();update_links();
  }
  if(e.code=="KeyR"){

    var select = document.getElementById('zoom_keep');
    
    if (select.checked==true){
      select.checked = false;
    }
    else{
      select.checked = true;
    }

  }
}
/*
q zoom out
w reset
e zoom in
a prev an
s toggle overlay (if not hidden) 
d next an
z 1st ori or b=0 (if not hidden)  
x 2ndr ori or b=1000  (if not hidden) 
c 3rd ori or b=2000  (if not hidden) 

*/

  function initDraw() {
    view.init()
    view.draw()
  }

  function resetDraw() {
    view.reset()
    view.draw()
  }

  function reDraw() {
    if(document.getElementById('zoom_keep').checked==true){
      resetDraw()
    }
    else{
      initDraw()
    }
  }


  function start(image) {
    canvas = document.getElementById('canvas')
    let img = document.getElementById(image);
    view = new Viewer(canvas, img)
    view.draw()
  }


  function updateTitle(){

    document.getElementById("analysis_title").innerHTML = document.getElementById("Analysis").options[document.getElementById("Analysis").selectedIndex].text.toUpperCase();

  }

  function updateImage(){

    var ana = document.getElementById("Analysis").value;
    var ord1 = document.getElementById("Order 1").checked;
    var ove = document.getElementById("Overlay check").checked;
    var ori = document.getElementById("Orientation").value;
    var bval = document.getElementById("b-value").value;

    if ((ana == "re")||(ana == "dre")||(ana == "Tre")||(ana == "wa")){
      document.getElementById("reg_opts").style.display="inline";
      document.getElementById("non_reg_opts").style.display="none";
      document.getElementById("EDDY_opts").style.display="none";
      document.getElementById("ori_opts").style.display="inline";
      if(ana == "Tre"){
        if (ord1 == true){
          ana = "Tre1"
        }
        else{
          ana = "Tre2"
        }
      }
      else if (ana == "wa"){
        if (ord1 == true){
          ana = "wa1"
        }
        else{
          ana = "wa2"
        }
      }
      else{
        if (ord1 == true){
          ana = "o1"
        }
        else{
          ana = "o2"
        }
      }
    }
    else if (ana.endsWith(".pdf")){

    }
    else if (ana=="dw" || ana=="cnr"){
      document.getElementById("reg_opts").style.display="none";
      document.getElementById("non_reg_opts").style.display="none";
      document.getElementById("EDDY_opts").style.display="inline";
      document.getElementById("ori_opts").style.display="none";
      
    }
    else if (ana.startsWith("dorz")){
      document.getElementById("reg_opts").style.display="none";
      document.getElementById("non_reg_opts").style.display="none";
      document.getElementById("EDDY_opts").style.display="none";
      document.getElementById("ori_opts").style.display="none";
      
    }

    else{
      document.getElementById("reg_opts").style.display="none";
      document.getElementById("non_reg_opts").style.display="inline";
      document.getElementById("EDDY_opts").style.display="none";
      document.getElementById("ori_opts").style.display="inline";
      if (ove == false){
        if(ana=="us" || ana == "ls" || ana == "dxc" || ana == "dfs" || ana == "dfsrb"){
          ana="under_sub"
        }
	else if(ana=="vbm"){
	  ana="under_vbm"
	}
        else if(ana=="Tbi"){
          ana="under_T2"
        }
        else if(ana=="dorf"){
          ana="under_dorf"
        }
        else if(ana=="dxs"){
          ana="dxc"
        }
        else{
          ana="under"
        }
      }
    }

    
    if (ana.endsWith(".pdf")){
      window.open(ana);
    }
      else{
      var new_img = ""


      if (ana=="dw" || ana=="cnr") {
        new_img =ana.concat('_',bval);
        
      }
      else if (ana.startsWith("dorz")) {
        new_img =ana;
        
      }
      else{
        new_img =ana.concat('_',ori);
      }
      

    if(document.getElementById('zoom_keep').checked==false){
      start(new_img);
    }
    else{
      let img = document.getElementById(new_img);
        view.setimage(img)
        view.draw()
    }
    document.getElementById("image_link").innerHTML = document.getElementById(new_img).src;
    document.getElementById("image_link").href = document.getElementById(new_img).src.substring(0,document.getElementById(new_img).src.lastIndexOf("/")+1);
}



    


  }


  window.addEventListener("error", function(e) {              // when an error happens
    if(e.target.tagName.toLowerCase() === "img") {          // if the target is an image
        e.target.src = "images/missing.png";                       // then change its src to whatever you want
    }
}, true);





