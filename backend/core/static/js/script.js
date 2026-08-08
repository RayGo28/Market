document.addEventListener('DOMContentLoaded', function() {
    // 1. Отримуємо дані з тегів json_script
    const labelsData = JSON.parse(document.getElementById('labels-data').textContent);
    const pricesData = JSON.parse(document.getElementById('prices-data').textContent);

    // 2. Знаходимо canvas
    const ctx = document.getElementById('cryptoChart').getContext('2d');

    // 3. Створюємо графік
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labelsData,
            datasets: [{
                label: 'Ціна',
                data: pricesData,
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointRadius: 2,
                pointBackgroundColor: '#10b981'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { color: '#9ca3af' }
                },
                y: {
                    grid: { color: '#333' },
                    ticks: { color: '#9ca3af' }
                }
            }
        }
    });
});