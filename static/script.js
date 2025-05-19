let temperatureChart;

async function fetchLatestTemperature() {
    try {
        const res = await fetch("/api/temperature");
        const data = await res.json();
        if (data.status === "success") {
            document.getElementById("latest-temp").textContent = `${data.temperature.toFixed(2)} °C`;
            document.getElementById("latest-time").textContent = new Date(data.timestamp).toLocaleString();
        } else {
            document.getElementById("latest-temp").textContent = "Ingen data tillgänglig.";
        }
    } catch (err) {
        console.error("Fel vid hämtning av temperatur:", err);
    }
}

async function fetchPrediction() {
    try {
        const res = await fetch("/api/predict");
        const data = await res.json();
        if (data.status === "success") {
            document.getElementById("prediction").textContent = `${data.predicted_temperature.toFixed(2)} °C`;
        } else {
            document.getElementById("prediction").textContent = "Ingen prediktion tillgänglig.";
        }
    } catch (err) {
        console.error("Fel vid hämtning av prediktion:", err);
    }
}

async function fetchTemperatureLogAndUpdateChart() {
    try {
        const res = await fetch("/api/temperature_log");
        const data = await res.json();

        if (data.status === "success") {
            const labels = data.temperatures.map(entry => new Date(entry.timestamp).toLocaleTimeString());
            const temps = data.temperatures.map(entry => entry.temperature);

            if (!temperatureChart) {
                const ctx = document.getElementById("temperatureChart").getContext("2d");
                temperatureChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Temperatur (°C)',
                            data: temps,
                            borderColor: 'rgb(75, 192, 192)',
                            tension: 0.3,
                            fill: true,
                            backgroundColor: 'rgba(75, 192, 192, 0.2)'
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: false
                            }
                        }
                    }
                });
            } else {
                // Uppdatera befintlig graf
                temperatureChart.data.labels = labels;
                temperatureChart.data.datasets[0].data = temps;
                temperatureChart.update();
            }
        }
    } catch (err) {
        console.error("Fel vid uppdatering av temperaturgraf:", err);
    }
}

function refreshData() {
    fetchLatestTemperature();
    fetchPrediction();
    fetchTemperatureLogAndUpdateChart();
}

refreshData(); // Kör direkt
setInterval(refreshData, 5000); // Uppdatera varje 5 sek
