window.setInterval(function() {
  let header = document.querySelector('header');
  header.style.visibility == 'hidden'
    ? header.style.visibility = 'visible' 
    : header.style.visibility = 'hidden';
}, 800);
