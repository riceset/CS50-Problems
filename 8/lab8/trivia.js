function changeColor()
{
  document.querySelector('#obama').onclick = function() {
    this.style.color = 'red';
    document.querySelector('#first').innerHTML = "Incorrect";
  }
  document.querySelector('#trump').onclick = function() {
    this.style.color = 'red';
    document.querySelector('#first').innerHTML = "Incorrect";
  }
  document.querySelector('#biden').onclick = function() {
    this.style.color = 'green';
    document.querySelector('#first').innerHTML = "Correct!";
  }
}

function checkAnswer()
{
  var answer = document.getElementById('box').value;
  alert(answer);

  document.querySelector('#check').onclick = function() {
    if (answer.toLowerCase() == 'russia') {
      document.querySelector('#second').innerHTML = "Correct";
    }
    else {
      document.querySelector('#second').innerHTML = "Incorrect";
    }
  }
}
