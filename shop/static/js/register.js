const form = document.querySelector("form"),
uField = form.querySelector(".username"),
uInput = uField.querySelector("input"),
pField = form.querySelector(".password"),
pInput = pField.querySelector("input"),
cField = form.querySelector(".confirm-password"),
cInput = cField.querySelector("input"),
eField = form.querySelector(".email"),
eInput = eField.querySelector("input");

// On form submission
form.onsubmit = (e) => {
  e.preventDefault(); // Prevent default form submission

  // Check if fields are empty, if so add error class, else check validity
  (uInput.value == "") ? uField.classList.add("shake", "error") : checkUsername();
  (pInput.value == "") ? pField.classList.add("shake", "error") : checkPass();
  (cInput.value == "") ? cField.classList.add("shake", "error") : checkConfirmPass();
  (eInput.value == "") ? eField.classList.add("shake", "error") : checkEmail();

  // Remove shake class after 500ms
  setTimeout(() => { 
    uField.classList.remove("shake");
    pField.classList.remove("shake");
    cField.classList.remove("shake");
    eField.classList.remove("shake");
  }, 500);

  // Check validity on keyup
  uInput.onkeyup = () => {checkUsername();} 
  pInput.onkeyup = () => {checkPass();}
  cInput.onkeyup = () => {checkConfirmPass();}
  eInput.onkeyup = () => {checkEmail();} 

  // Check username validity
  function checkUsername(){
    if(uInput.value == ""){ 
      uField.classList.add("error");
      uField.classList.remove("valid");
    } else { 
      uField.classList.remove("error");
      uField.classList.add("valid");
    }
  }

  // Check password validity
  function checkPass() {
    const result = zxcvbn(pInput.value); // Use zxcvbn library to check password strength
    let errorTxt = pField.querySelector(".error-txt");

    if (pInput.value === "") {
        pField.classList.add("error");
        pField.classList.remove("valid");
        errorTxt.innerText = "Password cannot be blank";
    } else if (result.score < 3) {
        pField.classList.add("error");
        pField.classList.remove("valid");
        if (result.feedback.warning === "") {
          errorTxt.innerText = "Password not long enough";
      } else {
          errorTxt.innerText = result.feedback.warning;
      }
    } else {
        pField.classList.remove("error");
        pField.classList.add("valid");
    }
  }

  // Check confirm password validity
  function checkConfirmPass() {
    let errorTxt = cField.querySelector(".error-txt");

    if (cInput.value === "") {
        cField.classList.add("error");
        cField.classList.remove("valid");
        errorTxt.innerText = "Confirm password cannot be blank";
    } else if (cInput.value !== pInput.value) {
        cField.classList.add("error");
        cField.classList.remove("valid");
        errorTxt.innerText = "Passwords don't match";
    } else {
        cField.classList.remove("error");
        cField.classList.add("valid");
    }
  }

  // Check email validity
  function checkEmail(){
    let pattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/; // Email regex pattern
    if(!eInput.value.match(pattern)){
      eField.classList.add("error");
      eField.classList.remove("valid");
      let errorTxt = eField.querySelector(".error-txt");
      (eInput.value != "") ? errorTxt.innerText = "Enter a valid email address" : errorTxt.innerText = "Email can't be blank";
    } else {
      eField.classList.remove("error");
      eField.classList.add("valid");
    }
  }

  // If no errors, submit the form
  if(!uField.classList.contains("error") && !pField.classList.contains("error") && !eField.classList.contains("error") && !cField.classList.contains("error")){
    form.submit(); 
  }
}