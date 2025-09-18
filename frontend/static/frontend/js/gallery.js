document.addEventListener('DOMContentLoaded', function() {
    const galleryItems = document.querySelectorAll('.gallery-item');
    const modal = document.querySelector('.gallery-modal');
    const modalImg = modal.querySelector('.modal-content img');
    const closeBtn = modal.querySelector('.modal-close');
    const prevBtn = modal.querySelector('.modal-prev');
    const nextBtn = modal.querySelector('.modal-next');
    let currentIndex = 0;

    // Open modal with clicked image
    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            currentIndex = parseInt(this.dataset.index);
            updateModalImage();
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    });

    // Close modal
    closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Navigate through images
    prevBtn.addEventListener('click', showPrevImage);
    nextBtn.addEventListener('click', showNextImage);

    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (!modal.classList.contains('active')) return;
        
        switch(e.key) {
            case 'ArrowLeft':
                showPrevImage();
                break;
            case 'ArrowRight':
                showNextImage();
                break;
            case 'Escape':
                closeModal();
                break;
        }
    });

    function updateModalImage() {
        const currentItem = document.querySelector(`[data-index="${currentIndex}"]`);
        modalImg.src = currentItem.querySelector('img').src;
        updateNavigationButtons();
    }

    function showPrevImage() {
        if (currentIndex > 0) {
            currentIndex--;
            updateModalImage();
        }
    }

    function showNextImage() {
        if (currentIndex < galleryItems.length - 1) {
            currentIndex++;
            updateModalImage();
        }
    }

    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    function updateNavigationButtons() {
        prevBtn.style.display = currentIndex === 0 ? 'none' : 'block';
        nextBtn.style.display = currentIndex === galleryItems.length - 1 ? 'none' : 'block';
    }
});