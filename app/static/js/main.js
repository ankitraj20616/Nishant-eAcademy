$(window).on("load", function () {
  $("#loginID").on("click", function (e) {
    e.preventDefault();
    $(".error").text("");
    $("#loginModal").modal();
  });

  $("#signUp").on("click", function (e) {
    $(".error").text("");
    $("#signUpModal").modal();
  });

  $("#signUpBtn").on("click", function (e) {
    e.preventDefault();
    if (validateSignUpInputs() == false) {
      $(".error").text("");
      $("#signUpModal").modal("hide");
      $("#verifyOtp").modal("show");
      const signupData = fetchSignUpData();
      $.post(`/send-otp/${signupData["phone_num"]}`);
    }
  });

  $("#loginBtn").on("click", function (e) {
    e.preventDefault();
    if (validateLoginInputs() == false) {
    }
  });

  $("#verify").on("click", function (e) {
    e.preventDefault();
    if (validateOtp() == false) {
      const signupData = fetchSignUpData();
      const otp = $("#otp").val();
      $.ajax({
        url: `/verify-otp?phone_num=${signupData["phone_num"]}&otp=${otp}`,
        type: "post",
        data: "",
        success: function (result) {
          if (result == true) {
            $.ajax({
              url: "/signUp",
              type: "post",
              data: JSON.stringify({
                first_name: signupData["first_name"],
                last_name: signupData["last_name"],
                phone_num: signupData["phone_num"],
                password: signupData["password"],
                confirm_password: signupData["confirm_password"],
                state: signupData["state"],
              }),
              contentType: "application/json",
              success: function () {
                alert("Sign Up Completed!");
              },
              error: function (error) {
                alert("Error occured: " + error.responseText);
              },
            });
          }
        },
        error: function (error) {
          alert("Error occured: " + error.responseText);
        },
      });
    } else {
      alert("Invalid Otp!");
    }
  });
});

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

  var state = $("#inputState").val();
  if (state === "Not_State") {
    $("#inputState").next(".error").text("Enter your state.");
    errorFlag = true;
  }

  return errorFlag;
}

function fetchSignUpData() {
  const signupData = {
    first_name: $("#inputFirstName").val(),
    last_name: $("#inputLastName").val(),
    phone_num: $("#phnNo").val(),
    password: $("#inputPassword").val(),
    confirm_password: $("#inputConfirmPassword").val(),
    state: $("#inputState").val(),
  };

  return signupData;
}

function validateOtp() {
  let errorFlag = false;
  let otp = $("#otp").val();
  if (otp === "") {
    $("#otp").next(".error").text("Invalid OTP!");
    errorFlag = true;
  }
  return errorFlag;
}
