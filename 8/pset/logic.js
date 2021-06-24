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

function changeImage() {
  if (document.getElementById("cat").src == "https://user-images.githubusercontent.com/48802655/123182497-f6109780-d465-11eb-8685-c27aabb6539e.jpg") 
  {
    document.getElementById("cat").src = "https://user-images.githubusercontent.com/48802655/123182105-20ae2080-d465-11eb-90fd-c3bdf9df264e.gif";
  }
  else 
  {
    document.getElementById("cat").src = "https://user-images.githubusercontent.com/48802655/123182497-f6109780-d465-11eb-8685-c27aabb6539e.jpg";
  }
}
