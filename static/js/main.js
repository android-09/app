document.addEventListener('DOMContentLoaded', function () {
  let hamburger = document.getElementById('sp__hamburger');
  let nav = document.getElementById('nav');

  hamburger.addEventListener('click', function () {
    hamburger.classList.toggle('active');
    nav.classList.toggle('active');
  });
});
