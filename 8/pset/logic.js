//Changes the greeting on the top of the screen
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
window.setInterval(changeLang, 900);

//Changes the image from the cat to the Rick Astley GIF
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

//Changes the color of the 'colors' button on the home screen
var j = 0;
function colorHome() {
  let button = document.querySelector('#colorfulbutton');
  let colors = [
    "#ff0000",
    "#00ff00",
    "#0000ff"
  ];
  button.style.backgroundColor = colors[j];
  j++;
  if (j == colors.length)
    j = 0;
}
window.setInterval(colorHome, 900);
