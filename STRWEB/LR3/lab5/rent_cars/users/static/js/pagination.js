document.addEventListener('DOMContentLoaded', function() {
    const carInfoWrappers = document.querySelectorAll('.car-info-wrapper');
    carInfoWrappers.forEach(wrapper => {
        const carInfo = wrapper.querySelector('.car-info');
        wrapper.addEventListener('mousemove', (event) => {
            const rect = wrapper.getBoundingClientRect();
            const x = event.clientX - rect.left; // Позиция мыши по X относительно карточки
            const y = event.clientY - rect.top; // Позиция мыши по Y относительно карточки
            const middleX = rect.width / 2;
            const middleY = rect.height / 2;
            const rotateX = ((y - middleY) / middleY) * 20;
            const rotateY = ((x - middleX) / middleX) * -20;
            carInfo.style.transition = 'transform 0.5s linear';
            carInfo.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });
        wrapper.addEventListener('mouseleave', () => {
            carInfo.style.transition = 'transform 0.5s ease';
            carInfo.style.transform = 'rotateX(0) rotateY(0)';
        });
    });
    const carsPerPage = 3;
    let currentPage = 1;

    const carContainer = document.querySelector('.car-grid');
    const cars = document.querySelectorAll('.no-highlight-link');
    const totalCars = cars.length;
    const totalPages = Math.ceil(totalCars / carsPerPage);

    const paginationControls = document.getElementById('pagination-controls');
    let isFirstDisplay = true;

    function displayCars() {
        if (isFirstDisplay) {
            carContainer.innerHTML = '';
            const start = (currentPage - 1) * carsPerPage;
            const end = start + carsPerPage;
            for (let i = start; i < end && i < totalCars; i++) {
                carContainer.appendChild(cars[i]);
            }
            updatePagination();
            isFirstDisplay = false;
        } else {
            carInfoWrappers.forEach(wrapper => {
                wrapper.style.animation = 'rotateOut 0.5s';
            });
            setTimeout(() => {
                carContainer.innerHTML = '';
                const start = (currentPage - 1) * carsPerPage;
                const end = start + carsPerPage;
                for (let i = start; i < end && i < totalCars; i++) {
                    carContainer.appendChild(cars[i]);
                }
                updatePagination();
                carInfoWrappers.forEach(wrapper => {
                    wrapper.style.animation = 'rotateIn 0.5s';
                });
            }, 500);
        }
    }

    function updatePagination() {
        paginationControls.innerHTML = '';
        const paginationButtons = document.createElement('div');
        paginationButtons.classList.add('pagination-buttons');
        paginationControls.appendChild(paginationButtons);
        const maxPagesToShow = 5;
        let startPage = Math.max(1, currentPage - Math.floor(maxPagesToShow / 2));
        let endPage = Math.min(totalPages, startPage + maxPagesToShow - 1);
        if (endPage - startPage + 1 < maxPagesToShow) {
            startPage = Math.max(1, endPage - maxPagesToShow + 1);
        }
        const prevButton = document.createElement('button');
        prevButton.innerHTML = '&#10094';
        prevButton.disabled = currentPage === 1;
        prevButton.addEventListener('click', () => {
            if (currentPage > 1) {
                currentPage--;
                displayCars();
            }
        });
        paginationButtons.appendChild(prevButton);
        for (let i = startPage; i <= endPage; i++) {
            const pageButton = document.createElement('button');
            pageButton.textContent = i;
            if (i === currentPage) {
                pageButton.disabled = true;
                pageButton.classList.add('active-page');
            }
            pageButton.addEventListener('click', () => {
                currentPage = i;
                displayCars();
            });
            paginationButtons.appendChild(pageButton);
        }
        const nextButton = document.createElement('button');
        nextButton.innerHTML = '&#10095';
        nextButton.disabled = currentPage === totalPages;
        nextButton.addEventListener('click', () => {
            if (currentPage < totalPages) {
                currentPage++;
                displayCars();
            }
        });
        paginationButtons.appendChild(nextButton);
    }

    displayCars();
});