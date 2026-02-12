function initRMChart(sessionMetrics) {
    const labels = Object.keys(sessionMetrics).sort();
    const data1rm = labels.map(d => sessionMetrics[d].estimated_1rm / 1000);
    const data5rm = labels.map(d => sessionMetrics[d].estimated_5rm / 1000);

    const ctx = document.getElementById('rmChart').getContext('2d');
    const rmChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Est. 1RM (kg)',
                    data: data1rm,
                    borderColor: '#3b82f6',
                    backgroundColor: '#3b82f6',
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    tension: 0.15,
                    fill: false,
                    hidden: false
                },
                {
                    label: 'Est. 5RM (kg)',
                    data: data5rm,
                    borderColor: '#22c55e',
                    backgroundColor: '#22c55e',
                    pointRadius: 5,
                    pointHoverRadius: 7,
                    tension: 0.15,
                    fill: false,
                    hidden: true
                }
            ]
        },
        options: {
            responsive: true,
            animation: { duration: 500 },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(ctx) {
                            return ctx.dataset.label + ': ' + ctx.parsed.y.toFixed(1) + ' kg';
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: { color: '#888' },
                    grid: { color: '#2a2a2a' }
                },
                y: {
                    ticks: {
                        color: '#888',
                        callback: function(v) { return v.toFixed(1) + ' kg'; }
                    },
                    grid: { color: '#2a2a2a' }
                }
            }
        }
    });

    return rmChart;
}

function showRM(rmChart, mode) {
    const btn1 = document.getElementById('btn-1rm');
    const btn5 = document.getElementById('btn-5rm');

    if (mode === '1rm') {
        rmChart.data.datasets[0].hidden = false;
        rmChart.data.datasets[1].hidden = true;
        btn1.style.background = '#3b82f6'; btn1.style.color = '#fff'; btn1.style.borderColor = '#3b82f6';
        btn5.style.background = 'transparent'; btn5.style.color = '#3b82f6'; btn5.style.borderColor = '#3b82f6';
    } else {
        rmChart.data.datasets[0].hidden = true;
        rmChart.data.datasets[1].hidden = false;
        btn5.style.background = '#22c55e'; btn5.style.color = '#fff'; btn5.style.borderColor = '#22c55e';
        btn1.style.background = 'transparent'; btn1.style.color = '#3b82f6'; btn1.style.borderColor = '#3b82f6';
    }

    rmChart.update();
}