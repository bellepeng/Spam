function updateScore(){
  const theEmail = document.getElementById('email_text').value;
  const outputElement = document.getElementById('output');
  if (theEmail.length < 15) {
      outputElement.textContent = 'Need more text to provide review';
      return;
  }

  $.ajax({
    type: 'POST',
    contentType: "application/json; charset=utf-8",
    url: '/spam_score',
    async: true,
    data: JSON.stringify({
      email: theEmail
    }),
    success: (response) => {
      outputElement.textContent = response.score;
      smile(response.score);
    },
    error: (response) => {
      outputElement.textContent = 'INVALID';
    }
  })
}
