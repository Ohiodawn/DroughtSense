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
    const resolvedLocation = document.getElementById('resolvedLocation');
    const largeRegionWarning = document.getElementById('largeRegionWarning');
    const retryLocation = document.getElementById('retryLocation');
    const downloadPdfBtn = document.getElementById('downloadPdfBtn');
    
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
    let lastResult = null;

    // Utilitarian Map Setup
    function initMap() {
        if (map) return;
        map = L.map('map', {
            zoomControl: true,
            scrollWheelZoom: false,
            dragging: true
        }).setView([0, 0], 2);
        
        L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; OpenStreetMap contributors',
            maxZoom: 20
        }).addTo(map);
    }

    function updateMap(lat, lon, name) {
        initMap();
        const coords = [lat, lon];
        map.setView(coords, 9);
        
        if (marker) {
            marker.setLatLng(coords).setPopupContent(name);
        } else {
            marker = L.marker(coords).addTo(map).bindPopup(name).openPopup();
        }
        
        setTimeout(() => map.invalidateSize(), 200);
    }

    // Handle Form submission
    assessForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const region = regionInput.value.trim();
        if (!region) return;

        // Enforce English (Latin) characters only
        const englishOnly = region.replace(/[^a-zA-Z0-9\s,\-]/g, "");
        if (englishOnly.length !== region.length || region.length < 2) {
            showError("System requires English (Latin) characters only (min 2 chars).");
            return;
        }

        hideAll();
        loadingSection.classList.remove('hidden');
        loadingStatus.textContent = "PROTOCOL: REGION_LOOKUP...";
        agentLogs.innerHTML = '';
        submitBtn.disabled = true;

        try {
            const response = await fetch('/api/geocode', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ region })
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'RESOLUTION_FAILED');

            if (data.matches.length === 1) {
                runAssessment(data.matches[0]);
            } else {
                showLocationSelector(data.matches);
            }
        } catch (err) {
            showError(err.message);
        } finally {
            submitBtn.disabled = false;
        }
    });

    function showLocationSelector(matches) {
        hideAll();
        matchList.innerHTML = '';
        matches.forEach(match => {
            const div = document.createElement('div');
            div.className = 'match-row';
            div.innerHTML = `
                <div>
                    <strong>${match.display_name}</strong><br>
                    <small style="color: #666;">COORDS: ${match.lat.toFixed(4)}, ${match.lon.toFixed(4)} | TYPE: ${match.type}</small>
                </div>
                <i class="fas fa-chevron-right"></i>
            `;
            div.onclick = () => runAssessment(match);
            matchList.appendChild(div);
        });
        locationSelector.classList.remove('hidden');
    }

    async function runAssessment(location) {
        hideAll();
        loadingSection.classList.remove('hidden');
        loadingStatus.textContent = "PROTOCOL: FETCH_NASA_DATA...";
        submitBtn.disabled = true;

        try {
            const response = await fetch('/api/assess', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ location })
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'ANALYSIS_FAILED');

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
            loadingStatus.textContent = `AGENT_${log.agent.toUpperCase()}: EXEC...`;
            const logEl = document.createElement('div');
            logEl.className = 'log-entry';
            logEl.innerHTML = `> [${new Date().toLocaleTimeString()}] ${log.agent}: ${log.status}`;
            agentLogs.appendChild(logEl);
            await new Promise(resolve => setTimeout(resolve, 600));
        }
    }

    function displayResults(data) {
        lastResult = data;
        const { location, climate_data, assessment } = data;
        
        resolvedLocation.textContent = `RESOLVED_ID: ${location.display_name}`;
        if (location.is_large) {
            largeRegionWarning.classList.remove('hidden');
        } else {
            largeRegionWarning.classList.add('hidden');
        }

        updateMap(location.lat, location.lon, location.name);

        resultRegion.textContent = location.name;
        explanationText.textContent = assessment.explanation;
        
        document.getElementById('tempVal').textContent = `${climate_data.temperature}°C`;
        document.getElementById('precipVal').textContent = `${climate_data.precipitation}mm`;
        document.getElementById('soilVal').textContent = `${Math.round(climate_data.soil_moisture * 100)}%`;

        riskBadge.textContent = `VULNERABILITY: ${assessment.risk_level}`;
        riskBadge.className = 'risk-badge ' + assessment.risk_level.toLowerCase();

        if (climate_data.daily_series) renderTrends(climate_data.daily_series);
        
        recommendationsList.innerHTML = '';
        assessment.recommendations.forEach(rec => {
            const div = document.createElement('div');
            div.className = 'rec-box';
            div.innerHTML = `<i class="fas fa-check-square"></i> <span>${rec}</span>`;
            recommendationsList.appendChild(div);
        });

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
        if (trendsChart) trendsChart.destroy();

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
                        label: 'PRECIP (mm)',
                        data: series.precip,
                        borderColor: '#2e7d32',
                        backgroundColor: 'rgba(46, 125, 50, 0.05)',
                        borderWidth: 2,
                        yAxisID: 'y',
                        fill: true,
                        pointRadius: 2,
                        tension: 0.1
                    },
                    {
                        label: 'TEMP (°C)',
                        data: series.temp,
                        borderColor: '#f4511e',
                        borderWidth: 2,
                        yAxisID: 'y1',
                        pointRadius: 2,
                        tension: 0.1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { type: 'linear', display: true, position: 'left', grid: { color: '#eee' } },
                    y1: { type: 'linear', display: true, position: 'right', grid: { display: false } }
                },
                plugins: { legend: { position: 'bottom' } }
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
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    downloadPdfBtn.addEventListener('click', async () => {
        if (!lastResult) return;
        downloadPdfBtn.disabled = true;
        const originalText = downloadPdfBtn.innerHTML;
        downloadPdfBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> EXPORTING...';

        try {
            const response = await fetch('/api/report', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(lastResult)
            });
            if (!response.ok) throw new Error('PDF_GEN_FAILED');
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `DS_Report_${lastResult.location.name}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
        } catch (err) {
            alert("ERROR: " + err.message);
        } finally {
            downloadPdfBtn.disabled = false;
            downloadPdfBtn.innerHTML = originalText;
        }
    });
});
