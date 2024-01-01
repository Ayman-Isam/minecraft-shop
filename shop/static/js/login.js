const form = document.querySelector("form"),
uField = form.querySelector(".username"),
uInput = uField.querySelector("input"),
pField = form.querySelector(".password"),
pInput = pField.querySelector("input");

form.onsubmit = (e)=>{
  e.preventDefault(); 

  // Validate username and password fields
  (uInput.value == "") ? uField.classList.add("shake", "error") : checkUsername();
  (pInput.value == "") ? pField.classList.add("shake", "error") : checkPass();

  // Remove "shake" class after 500ms
  setTimeout(()=>{ 
    uField.classList.remove("shake");
    pField.classList.remove("shake");
  }, 500);

  // Validate fields on keyup
  uInput.onkeyup = ()=>{checkUsername();} 
  pInput.onkeyup = ()=>{checkPass();}

  // Validate username
  function checkUsername(){
    if(uInput.value == ""){ 
      uField.classList.add("error");
      uField.classList.remove("valid");
    }else{ 
      uField.classList.remove("error");
      uField.classList.add("valid");
    }
  }

  // Validate password
  function checkPass(){ 
    if(pInput.value == ""){ 
      pField.classList.add("error");
      pField.classList.remove("valid");
    }else{ 
      pField.classList.remove("error");
      pField.classList.add("valid");
    }
  }

  // Submit form if validation passes
  if(!uField.classList.contains("error") && !pField.classList.contains("error")){
    form.submit(); 
  }
}