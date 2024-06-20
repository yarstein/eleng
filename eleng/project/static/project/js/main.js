var slideIndex = 1;
showSlides(slideIndex);

// Вперед/назад элементы управления
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Элементы управления миниатюрами изображений
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}

// автоматическая прокрутка каждые 5 секунд
var autoSlideInterval = setInterval(function() {
    plusSlides(1);
}, 5000); // 5000 мс = 5 секунд

// Остановка автоматической прокрутки при наведении мыши
var slideshowContainer = document.querySelector('.slideshow-container');
slideshowContainer.addEventListener('mouseenter', function() {
    clearInterval(autoSlideInterval);
});
slideshowContainer.addEventListener('mouseleave', function() {
    autoSlideInterval = setInterval(function() {
        plusSlides(1);
    }, 5000);
});