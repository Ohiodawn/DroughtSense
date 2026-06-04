document.addEventListener('DOMContentLoaded', () => {
    const assessForm = document.getElementById('assessForm');
    const regionInput = document.getElementById('regionInput');
    const submitBtn = document.getElementById('submitBtn');
    
    const locationSelector = document.getElementById('locationSelector');
    const matchList = document.getElementById('matchList');
    
    const loadingSection = document.getElementById('loading');
    const loadingStatus = document.getElementById('loadingStatus');
    const agentLogs = document.getElementById('agentLogs');
    
    const resultSection = document.getElementById('result');
    const locationBanner = document.getElementById('locationBanner');
    const resolvedLocation = document.getElementById('resolvedLocation');
    const largeRegionWarning = document.getElementById('largeRegionWarning');
    const retryLocation = document.getElementById('retryLocation');
    
    const resultRegion = document.getElementById('resultRegion');
    const riskBadge = document.getElementById('riskBadge');
    const explanationText = document.getElementById('explanationText');
    const recommendationsList = document.getElementById('recommendationsList');
    const citationsSection = document.getElementById('citationsSection');
    const citationsText = document.getElementById('citationsText');
    const errorSection = document.getElementById('error');

    let trendsChart = null;
    let map = null;
    let marker = null;

    // Initialize Map
    function initMap() {
        if (map) return;
        map = L.map('map').setView([0, 0], 2);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);
    }

    function updateMap(lat, lon, name) {
        initMap();
        const coords = [lat, lon];
        map.setView(coords, 8);
        
        if (marker) {
            marker.setLatLng(coords).setPopupContent(name);
        } else {
            marker = L.marker(coords).addTo(map).bindPopup(name).openPopup();
        }
        
        // Fix Leaflet sizing issue in hidden containers
        setTimeout(() => {
            map.invalidateSize();
        }, 100);
    }

    // Handle initial form submission (Geocoding Step)
    assessForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        let region = regionInput.value.trim();
        if (!region) return;

        // Reset UI
        hideAll();
        loadingSection.classList.remove('hidden');
        loadingStatus.textContent = "Resolving location...";
        agentLogs.innerHTML = '';
        submitBtn.disabled = true;

        try {
            const response = await fetch('/api/geocode', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ region })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Geocoding failed');
            }

            if (data.matches.length === 1) {
                // Single match: auto-proceed to assessment
                runAssessment(data.matches[0]);
            } else {
                // Multiple matches: show selector
                showLocationSelector(data.matches);
            }

        } catch (err) {
            showError(err.message);
        } finally {
            if (locationSelector.classList.contains('hidden') && resultSection.classList.contains('hidden')) {
                loadingSection.classList.add('hidden');
            }
            submitBtn.disabled = false;
        }
    });

    function showLocationSelector(matches) {
        hideAll();
        matchList.innerHTML = '';
        matches.forEach(match => {
            const div = document.createElement('div');
            div.className = 'match-item';
            div.innerHTML = `<strong>${match.display_name}</strong><br><small>${match.type} · ${match.lat.toFixed(2)}°N, ${match.lon.toFixed(2)}°E</small>`;
            div.onclick = () => runAssessment(match);
            matchList.appendChild(div);
        });
        locationSelector.classList.remove('hidden');
    }

    async function runAssessment(location) {
        hideAll();
        loadingSection.classList.remove('hidden');
        loadingStatus.textContent = "Connecting to NASA POWER API...";
        submitBtn.disabled = true;

        try {
            const response = await fetch('/api/assess', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ location })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to generate assessment');
            }

            await showAgentLogs(data.agent_logs);
            displayResults(data);

        } catch (err) {
            showError(err.message);
        } finally {
            loadingSection.classList.add('hidden');
            submitBtn.disabled = false;
        }
    }

    async function showAgentLogs(logs) {
        agentLogs.innerHTML = '';
        for (const log of logs) {
            loadingStatus.textContent = log.status;
            const logEl = document.createElement('div');
            logEl.className = 'log-entry';
            logEl.innerHTML = `> [${log.agent}] ${log.status}`;
            agentLogs.appendChild(logEl);
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }

    function displayResults(data) {
        const { location, climate_data, assessment } = data;
        
        // Location Info
        resolvedLocation.textContent = `${location.display_name} (${location.lat.toFixed(2)}°N, ${location.lon.toFixed(2)}°E)`;
        if (location.is_large) {
            largeRegionWarning.classList.remove('hidden');
        } else {
            largeRegionWarning.classList.add('hidden');
        }

        updateMap(location.lat, location.lon, location.name);

        resultRegion.textContent = location.name || "Target Region";
        explanationText.textContent = assessment.explanation;
        
        // Climate Stats
        document.getElementById('tempVal').textContent = climate_data.temperature;
        document.getElementById('precipVal').textContent = climate_data.precipitation;
        document.getElementById('soilVal').textContent = Math.round(climate_data.soil_moisture * 100);

        // Risk Badge
        riskBadge.textContent = `${assessment.risk_level} Risk`;
        riskBadge.className = 'badge ' + assessment.risk_level.toLowerCase();
        
        // Render Trends Chart
        if (climate_data.daily_series) {
            renderTrends(climate_data.daily_series);
        }

        // Recommendations
        recommendationsList.innerHTML = '';
        assessment.recommendations.forEach(rec => {
            const li = document.createElement('li');
            li.innerHTML = `<i class="fas fa-check-circle"></i> ${rec}`;
            recommendationsList.appendChild(li);
        });

        // Citations
        if (assessment.citations && assessment.citations !== "None") {
            citationsText.textContent = assessment.citations;
            citationsSection.classList.remove('hidden');
        } else {
            citationsSection.classList.add('hidden');
        }

        resultSection.classList.remove('hidden');
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }

    function renderTrends(series) {
        const ctx = document.getElementById('trendsChart').getContext('2d');
        
        if (trendsChart) {
            trendsChart.destroy();
        }

        const labels = series.dates.map(d => {
            const m = d.substring(4, 6);
            const day = d.substring(6, 8);
            return `${m}/${day}`;
        });

        trendsChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Rainfall (mm)',
                        data: series.precip,
                        borderColor: '#2e7d32',
                        backgroundColor: 'rgba(46, 125, 50, 0.1)',
                        borderWidth: 2,
                        yAxisID: 'y',
                        fill: true,
                        tension: 0.3
                    },
                    {
                        label: 'Temp (°C)',
                        data: series.temp,
                        borderColor: '#f44336',
                        borderWidth: 2,
                        yAxisID: 'y1',
                        tension: 0.3
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: { display: true, text: 'Rainfall (mm)' }
                    },
                    y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        grid: { drawOnChartArea: false },
                        title: { display: true, text: 'Temp (°C)' }
                    }
                }
            }
        });
    }

    function showError(msg) {
        hideAll();
        errorSection.querySelector('.error-message').textContent = msg;
        errorSection.classList.remove('hidden');
    }

    function hideAll() {
        locationSelector.classList.add('hidden');
        loadingSection.classList.add('hidden');
        resultSection.classList.add('hidden');
        errorSection.classList.add('hidden');
    }

    retryLocation.onclick = (e) => {
        e.preventDefault();
        hideAll();
        regionInput.focus();
        regionInput.select();
    };
});
