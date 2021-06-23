window.setInterval(function() {
  let body = document.querySelector('header');

  let greetings = [
    "Hola Mundo!",
    "Bonjour le Monde!",
    "你好世界!"
  ]

  for (let i = 0; i < greetings.length; i++)
  {
    body.innerHTML = greetings[i];

    if (i == greetings.length - 1)
      i = 0;
  }
}, 500);
