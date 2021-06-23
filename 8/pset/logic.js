var i = 0;

function changeLang() {

  let body = document.querySelector('header');

  let greetings = [
    "Hola Mundo!",
    "Bonjour le Monde!",
    "Hello World!"
  ];

  body.innerHTML = greetings[i];

  i++;

  if (i == greetings.length)
    i = 0;
}
