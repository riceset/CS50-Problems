var i = 0;

function changeLang() {
  let body = document.querySelector('header');
  let greetings = [
    "Hola Mundo!",
    "Bonjour le Monde!",
    "Hello World!",
    "Ciao mondo!",
  ];
  body.innerHTML = greetings[i];
  i++;
  if (i == greetings.length)
    i = 0;
}

window.setInterval(changeLang, 700);
