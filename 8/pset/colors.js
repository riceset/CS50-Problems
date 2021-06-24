var i = 0;

function changeColor() {
  let body = document.querySelector('body');

  let colors = [
    '#ff0000',
    '#00ff00',
    '#0000ff'
  ];

  body.style.backgroundColor = colors[i];

  i++;

  if (i == colors.length)
    i = 0;
}

window.setInterval(changeColor, 500);
