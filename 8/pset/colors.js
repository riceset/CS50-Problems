var i = 0;
var j = 0;

function changeColor() {
  let body = document.querySelector('body');
  let colors = [
    '#ff0000',
    '#00ff00',
    '#0000ff',
  ];
  body.style.backgroundColor = colors[i];
  i++;
  if (i == colors.length)
    i = 0;
}

function changeText() {
  let text = document.querySelector('#text');
  let colors = [
    "Red",
    "Green",
    "Blue",
  ];
  text.innerHTML = colors[j];
  j++;
  if (j == colors.length)
    j = 0;
}

window.setInterval(changeColor, 700);
window.setInterval(changeText, 700);
