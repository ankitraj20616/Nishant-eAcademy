$(document).on("load", function () {
  $("#loginID").on("click", function (e) {
    e.preventDefault();
    $(".error").text("");
    $("#loginModal").modal();
  });

  $("#signUp").on("click", function (e) {
    $(".error").text("");
    $("#signUpModal").modal();
  });

  $("#signUpBtn").on("click", function () {
    e.preventDefault();
    console.log(this);
    // if (validateSignUpInputs() == false) {
    // }
  });

  $("#loginBtn").on("click", function (e) {
    e.preventDefault();
    if (validateLoginInputs() == false) {
    }
  });

  $("#verify").on("click", function (e) {
    e.preventDefault();
    if (validateOTPInputs() == false) {
    }
  });
});

function validateOTPInputs() {
  var errorFlag = false;

  var emailValue = $("#opt").val();
  if (emailValue === "") {
    $("#opt").next(".error").text("OPT is required.");
    errorFlag = true;
  }
  return errorFlag;
}

function validateLoginInputs() {
  var errorFlag = false;

  var emailValue = $("#loginEmail").val();
  if (emailValue === "") {
    $("#loginEmail").next(".error").text("Email ID is required.");
    errorFlag = true;
  } else if (IsEmail(emailValue) === false) {
    $("#loginEmail").next(".error").text("Entered Email is not Valid!!");
    errorFlag = true;
  }
  return errorFlag;
}

function validateSignUpInputs() {
  var errorFlag = false;

  var inputFirstName = $("#inputFirstName").val();
  if (inputFirstName === "") {
    $("#inputFirstName").next(".error").text("First Name is required.");
    errorFlag = true;
  }

  var inputLastName = $("#inputLastName").val();
  if (inputLastName === "") {
    $("#inputLastName").next(".error").text("Last Name is required.");
    errorFlag = true;
  }

  var passwordValue = $("#inputPassword").val();
  if (passwordValue === "") {
    $("#inputPassword").next(".error").text("Password is required.");
    errorFlag = true;
  }

  var confirmPassword = $("#inputConfirmPassword").val();
  if (confirmPassword === "") {
    $("#inputConfirmPassword")
      .next(".error")
      .text("Confirm password is required.");
    errorFlag = true;
  } else if (confirmPassword !== passwordValue) {
    $("#inputConfirmPassword")
      .next(".error")
      .text("Password and Confirm must match!");
    errorFlag = true;
  }

  var phoneValue = $("#phnNo").val();
  if (phoneValue === "") {
    $("#phnNo").next(".error").text("Phone No is required.");
    errorFlag = true;
  }

  return false;
}
