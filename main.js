document.addEventListener(
  'DOMContentLoaded', function() {
     var container = document.querySelector('.container');
     var items = container.querySelectorAll('.item');

     if (items.length < 3) {
        container.style.width = 'fit-content';
        container.style.margin = '0 auto 100px';
  }
});