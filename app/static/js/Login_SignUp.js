"use strict";
const loginFrom = document.querySelector(".login-form");
const signUpForm = document.querySelector("#signUpForm");
const loginBtn = document.getElementById("loginBtn");
const signUpBtn = document.getElementById("signUpBtn");
const buttonContainer = document.querySelector(".button_container");
const otpForm = document.getElementById("otpForm");
const otpErrorDiv = document.getElementById("OTPError");
const signUpDone = document.getElementById("SignUpDone");
const signUpSubmit = document.getElementById("submitSignUp");
const otpSubmitBtn = document.getElementById("otpSubmit");

const starter = function () {
  loginFrom.classList.add("hidden");
  signUpForm.classList.add("hidden");
  otpForm.classList.add("hidden");
  otpErrorDiv.classList.add("hidden");
  signUpDone.classList.add("hidden");
};

$("#otpSubmit").click(function () {
  console.log(121);
});

starter();

loginBtn.addEventListener("click", function () {
  loginFrom.classList.remove("hidden");
  buttonContainer.classList.add("hidden");
  signUpForm.classList.add("hidden");
});
signUpBtn.addEventListener("click", function () {
  signUpForm.classList.remove("hidden");
  buttonContainer.classList.add("hidden");
  loginFrom.classList.add("hidden");
});
document.addEventListener("click", function (event) {
  const isClickLoginFrom = loginFrom.contains(event.target);
  const isClickSignUpFrom = signUpForm.contains(event.target);
  const isClickInsideButton = buttonContainer.contains(event.target);

  if (!isClickLoginFrom && !isClickSignUpFrom && !isClickInsideButton) {
    loginFrom.classList.add("hidden");
    signUpForm.classList.add("hidden");
    buttonContainer.classList.remove("hidden");
  }
});

signUpSubmit.addEventListener("click", async function (event) {
  event.preventDefault();

  const firstName = document.getElementById("first-name").value;
  const lastName = document.getElementById("last-name").value;
  const phoneNumber = document.getElementById("phn-num").value;
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm-password").value;
  const state = document.getElementById("state").value;

  const requestData = {
    first_name: firstName,
    last_name: lastName,
    phone_num: phoneNumber,
    password: password,
    confirm_password: confirmPassword,
    state: state,
  };

  try {
    const isOTPSent = await fetch(`/send-otp/${requestData["phone_num"]}`, {
      method: "POST",
    });

    if (!isOTPSent.ok) {
      signUpForm.classList.add("hidden");
      otpErrorDiv.classList.remove("hidden");
      throw new Error(`Error in sending Otp: ${isOTPSent.status}`);
    } else {
      signUpForm.classList.add("hidden");
      otpErrorDiv.classList.add("hidden");
      otpForm.classList.remove("hidden");

      // otpSubmitBtn.addEventListener("click", async function (event) {
      //   event.preventDefault();

      //   const otpValue = document.getElementById("userOtp").value;
      //   console.log(otpValue);

      //   try {
      //     const verifyOtpResponse = await fetch(
      //       `/verify-otp?phone_num=${requestData["phone_num"]}&otp=${otpValue}`,
      //       {
      //         method: "POST",
      //       }
      //     );
      //     if (!verifyOtpResponse.ok) {
      //       signUpForm.classList.add("hidden");
      //       otpForm.classList.add("hidden");
      //       otpErrorDiv.classList.remove("hidden");
      //       throw new Error(
      //         `Error in verifying Otp: ${verifyOtpResponse.status}`
      //       );
      //     } else {
      //       const signUpResponse = await fetch("/signUp", {
      //         method: "POST",
      //         headers: { "Content-Type": "application/json" },
      //         body: JSON.stringify(requestData),
      //       });

      //       if (signUpResponse.ok) {
      //         signUpForm.classList.add("hidden");
      //         otpForm.classList.add("hidden");
      //         signUpDone.classList.remove("hidden");
      //         const result = await signUpResponse.json();
      //         console.log(result);
      //       } else {
      //         signUpForm.classList.add("hidden");
      //         otpForm.classList.add("hidden");
      //         otpErrorDiv.classList.remove("hidden");
      //         const error = await signUpResponse.json();
      //         console.log(`Error in Siging Up: ${error}`);
      //       }
      //     }
      //   } catch (error) {
      //     console.error("Error in Verifying OTP:", error);
      //   }
      // });
    }
  } catch (error) {
    console.error("Error in Sending OTP:", error);
  }
});
