function changeColor(answer)
{
  document.querySelector('#obama').onclick = function() {
    this.style.color = 'red';
  }
  document.querySelector('#trump').onclick = function() {
    this.style.color = 'red';
  }
  document.querySelector('#biden').onclick = function() {
    this.style.color = 'green';
  }
}
