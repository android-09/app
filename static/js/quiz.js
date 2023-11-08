let submitButton = document.getElementById("submit-button");

submitButton.addEventListener("click", function (event) {
  event.preventDefault();

  let userAnswer = document.querySelector(
    'input[name="user_answer"]:checked'
  ).value;
  let correctAnswer = quizData[3];

  let correctFeedback = document.getElementById("correct-feedback");
  let incorrectFeedback = document.getElementById("incorrect-feedback");

  if (userAnswer === correctAnswer) {
    correctFeedback.style.display = "block";
    incorrectFeedback.style.display = "none";
  } else {
    incorrectFeedback.style.display = "block";
    correctFeedback.style.display = "none";
  }

  setTimeout(function () {
    document.querySelector("form").submit();
  }, 1200);
});
