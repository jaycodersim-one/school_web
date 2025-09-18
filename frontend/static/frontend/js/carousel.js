document.addEventListener('DOMContentLoaded', function() {
    const track = document.querySelector('.carousel-track');
    const slides = Array.from(track.children);
    const nextButton = document.querySelector('.next-button');
    const prevButton = document.querySelector('.prev-button');
    const dotsContainer = document.querySelector('.carousel-dots');

    const slideWidth = slides[0].getBoundingClientRect().width;
    const slidesToShow = 3;
    const slidesToScroll = 3;

    // Position slides next to each other
    function setSlidePosition() {
        slides.forEach((slide, index) => {
            slide.style.left = slideWidth * index + 'px';
        });
    }

    // Create navigation dots
    function createDots() {
        const numberOfDots = Math.ceil(slides.length / slidesToShow);
        for (let i = 0; i < numberOfDots; i++) {
            const dot = document.createElement('div');
            dot.classList.add('carousel-dot');
            if (i === 0) dot.classList.add('active');
            dot.addEventListener('click', () => {
                moveToSlide(i * slidesToShow);
                updateDots(i);
            });
            dotsContainer.appendChild(dot);
        }
    }

    // Update active dot
    function updateDots(currentIndex) {
        const dots = Array.from(dotsContainer.children);
        dots.forEach(dot => dot.classList.remove('active'));
        const activeDotIndex = Math.floor(currentIndex / slidesToShow);
        dots[activeDotIndex].classList.add('active');
    }

    // Move slides
    function moveToSlide(targetIndex) {
        track.style.transform = `translateX(-${targetIndex * slideWidth}px)`;
        currentIndex = targetIndex;
        updateButtons();
    }

    // Update button states
    function updateButtons() {
        prevButton.style.opacity = currentIndex === 0 ? '0.5' : '1';
        nextButton.style.opacity = currentIndex >= slides.length - slidesToShow ? '0.5' : '1';
        prevButton.disabled = currentIndex === 0;
        nextButton.disabled = currentIndex >= slides.length - slidesToShow;
    }

    // Initialize carousel
    let currentIndex = 0;
    setSlidePosition();
    createDots();
    updateButtons();

    // Event listeners
    nextButton.addEventListener('click', () => {
        if (currentIndex < slides.length - slidesToShow) {
            moveToSlide(currentIndex + slidesToScroll);
            updateDots(currentIndex);
        }
    });

    prevButton.addEventListener('click', () => {
        if (currentIndex > 0) {
            moveToSlide(currentIndex - slidesToScroll);
            updateDots(currentIndex);
        }
    });

    // Auto-advance carousel
    let autoAdvance = setInterval(() => {
        if (currentIndex < slides.length - slidesToShow) {
            moveToSlide(currentIndex + slidesToScroll);
            updateDots(currentIndex);
        } else {
            moveToSlide(0);
            updateDots(0);
        }
    }, 5000);

    // Pause auto-advance on hover
    track.addEventListener('mouseenter', () => {
        clearInterval(autoAdvance);
    });

    track.addEventListener('mouseleave', () => {
        autoAdvance = setInterval(() => {
            if (currentIndex < slides.length - slidesToShow) {
                moveToSlide(currentIndex + slidesToScroll);
                updateDots(currentIndex);
            } else {
                moveToSlide(0);
                updateDots(0);
            }
        }, 5000);
    });
});