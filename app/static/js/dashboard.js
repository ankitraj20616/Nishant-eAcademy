$(window).on("load", function () {
  // Open modal on button click
  $("#addCourseBtn").on("click", function () {
    $("#addCourseModal").removeClass("hidden");
  });

  // Close modal on button click
  $("#closeModalBtn").on("click", function () {
    $("#addCourseModal").addClass("hidden");
  });
});
