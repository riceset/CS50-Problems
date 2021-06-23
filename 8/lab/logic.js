document.addEventListener('DOMContentLoaded', function() {
  //The correct answer button
  let correct = document.querySelector('.correct');

  //listens for the click event on the button
  correct.addEventListener('click', function() {

    //When the button is clicked, change its color and display the answer underneath it
    correct.style.backgroundColor = 'green';
    document.querySelector('#answer').innerHTML = 'Correct';
  });

  //An array of all the incorrect answer buttons
  let incorrects = document.querySelectorAll('.incorrect');

  for (let button of incorrects) {
    button.addEventListener('click', function() {
      button.style.backgroundColor = 'red';
      document.querySelector('#answer').innerHTML = 'Incorrect';
    });
  }

  document.querySelector('#check').addEventListener('click', function() {
    //
    let input = document.querySelector('input');

    //Lowercases the input and compares
    if (input.value.toLowerCase() == 'russia') {
      input.style.backgroundColor = 'green';
      document.querySelector('#answer2').innerHTML = 'Correct!';
    }
    else {
      input.style.backgroundColor = 'red';
      document.querySelector('#answer2').innerHTML = 'Incorrect';
    }
  });
});
