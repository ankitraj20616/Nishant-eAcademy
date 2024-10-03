"use strict";
const loginFrom = document.querySelector(".login-form");
const signUpForm = document.querySelector(".sign-up-form");
const loginBtn = document.getElementById("loginBtn");
const signUpBtn = document.getElementById("signUpBtn");
const buttonContainer = document.querySelector(".button_container");

const starter = function () {
  loginFrom.classList.add("hidden");
  signUpForm.classList.add("hidden");
};

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
