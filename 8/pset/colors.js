var i = 0;

function changeLang() {
  let body = document.querySelector('body');
  let colors = [
    '#ff0000',
    '#00ff00',
    '0000ff'
  ];

  body.style.backgroundColor = colors[i];
  i++;
  if (i == greetings.length)
    i = 0;
}
