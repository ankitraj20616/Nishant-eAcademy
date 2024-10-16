$(document).ready(function(){

  $("#loginID").click(function(){
    $(".error").text('')
    $("#loginModal").modal();
  });

  $("#signUp").click(function(){
    $(".error").text('')
    $("#signUpModal").modal();
  });


  $("#signUpBtn").click(function(e){
    e.preventDefault();
    if (validateSignUpInputs() == false) {


    }
  });

  $("#loginBtn").click(function(e){
    e.preventDefault();
    if (validateLoginInputs() == false) {


    }
  });

  $("#verify").click(function(e){
    e.preventDefault();
    if (validateOTPInputs() == false) {


    }
  });
});

function validateOTPInputs(){
    var errorFlag = false

    var emailValue = $("#opt").val();
    if(emailValue === '') {
        $("#opt").next('.error').text("OPT is required.")
        errorFlag = true
    }
    return errorFlag
}

function validateLoginInputs(){
    var errorFlag = false

    var emailValue = $("#loginEmail").val();
    if(emailValue === '') {
        $("#loginEmail").next('.error').text("Email ID is required.")
        errorFlag = true
    }
    else if (IsEmail(emailValue) === false) {
        $("#loginEmail").next('.error').text("Entered Email is not Valid!!");
        errorFlag = true
    }
    return errorFlag
}

function validateSignUpInputs(){
    var errorFlag = false

    var emailValue = $("#inputEmail").val();
    if(emailValue === '') {
        $("#inputEmail").next('.error').text("Email ID is required.")
        errorFlag = true
    }
    else if (IsEmail(emailValue) === false) {
        $("#inputEmail").next('.error').text("Entered Email is not Valid!!");
        errorFlag = true
    }

    var passwordValue = $("#inputPassword").val();
    if(passwordValue === '') {
        $("#inputPassword").next('.error').text("Password is required.")
        errorFlag = true
    }

    var phoneValue = $("#phnNo").val();
    if(phoneValue === '') {
        $("#phnNo").next('.error').text("Phone No is required.")
        errorFlag = true
    }

    return errorFlag
}

function IsEmail(email) {
    const regex = /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if (!regex.test(email)) {
        return false;
    }
    else {
        return true;
    }
}