async function fetchRentalData() {
    try {
        const response = await fetch('/api/rentals-per-model/');
        if (!response.ok) {
            throw new Error('Ошибка при получении данных');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

async function drawRentalChart() {
    const data = await fetchRentalData();

    if (data) {
        const ctx = document.getElementById('rentalChart').getContext('2d');
        const backgroundColors = data.labels.map(() => {
            return `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.6)`;
        });
        const borderColors = backgroundColors.map(color => color.replace('0.6', '1'));
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Количество аренд',
                    data: data.rentalCounts,
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 1
                }]
            },
            options: {
                animation: {
                    duration: 2000,
                    easing: 'easeInOutBounce'
                },
                scales: {
                    x: { title: { display: true, text: 'Модель машины' } },
                    y: { title: { display: true, text: 'Количество аренд' }, beginAtZero: true }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }
}

drawRentalChart();