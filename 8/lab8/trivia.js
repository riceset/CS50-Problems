document.addEventListener('DOMContentLoaded', function() {

});

function changeColor()
{
  document.querySelector('#obama').onclick = function() {
    this.style.color = 'red';
    document.querySelector('#answer').innerHTML = "Incorrect";
  }
  document.querySelector('#answer').onclick = function() {
    this.style.color = 'red';
    document.querySelector('#answer').innerHTML = "Incorrect";
  }
  document.querySelector('#biden').onclick = function() {
    this.style.color = 'green';
    document.querySelector('#answer').innerHTML = "Correct!";
  }
}

function checkAnswer()
{
  var answer = document.getElementById('box').value;
  alert(answer);

  document.querySelector('#check').onclick = function() {
    if (answer.toLowerCase() == 'russia') {
      document.querySelector('#answer2').innerHTML = "Correct";
    }
    else {
      document.querySelector('#second').innerHTML = "Incorrect";
    }
  }
}
