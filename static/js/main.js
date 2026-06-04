document.addEventListener('DOMContentLoaded', () => {
    console.log("DroughtSense System Initialized.");

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

    // Utilitarian Map Setup with Safety
    function initMap() {
        if (map) return;
        if (typeof L === 'undefined') {
            console.error("Leaflet library not loaded.");
            return;
        }
        try {
            map = L.map('map', {
                zoomControl: true,
                scrollWheelZoom: false,
                dragging: true
            }).setView([0, 0], 2);
            
            L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; OpenStreetMap contributors',
                maxZoom: 20
            }).addTo(map);
        } catch (e) {
            console.error("Map initialization failed: ", e);
        }
    }

    function updateMap(lat, lon, name, isLarge) {
        initMap();
        if (!map) return;
        
        try {
            const coords = [lat, lon];
            // Adaptive zoom: Cities (11), Large States/Provinces (6)
            const zoom = isLarge ? 6 : 11;
            map.setView(coords, zoom);
            
            if (marker) {
                marker.setLatLng(coords).setPopupContent(name);
            } else {
                marker = L.marker(coords).addTo(map).bindPopup(name).openPopup();
            }
            
            setTimeout(() => map.invalidateSize(), 200);
        } catch (e) {
            console.error("Map update failed: ", e);
        }
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
            console.log("Executing Geocoding for: ", region);
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
            console.error("Submission Error: ", err);
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
            console.log("Executing Assessment for Coords: ", location.lat, location.lon);
            const response = await fetch('/api/assess', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ location })
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'ANALYSIS_FAILED');

            // Set state immediately for PDF/export functionality
            lastResult = data;

            await showAgentLogs(data.agent_logs);
            displayResults(data);
        } catch (err) {
            console.error("Assessment Error: ", err);
            showError(err.message);
        } finally {
            loadingSection.classList.add('hidden');
            submitBtn.disabled = false;
        }
    }

    async function showAgentLogs(logs) {
        if (!logs || !Array.isArray(logs)) return;
        agentLogs.innerHTML = '';
        for (const log of logs) {
            loadingStatus.textContent = `AGENT_${log.agent.toUpperCase()}: EXEC...`;
            const logEl = document.createElement('div');
            logEl.className = 'log-entry';
            logEl.innerHTML = `> [${new Date().toLocaleTimeString()}] ${log.agent}: ${log.status}`;
            agentLogs.appendChild(logEl);
            await new Promise(resolve => setTimeout(resolve, 800));
        }
    }

    function displayResults(data) {
        const { location, climate_data, assessment } = data;
        
        resolvedLocation.textContent = `RESOLVED_ID: ${location.display_name}`;
        if (location.is_large) {
            largeRegionWarning.classList.remove('hidden');
        } else {
            largeRegionWarning.classList.add('hidden');
        }

        updateMap(location.lat, location.lon, location.name, location.is_large);

        resultRegion.textContent = location.name;
        explanationText.textContent = assessment.explanation;
        
        document.getElementById('tempVal').textContent = `${climate_data.temperature}°C`;
        document.getElementById('precipVal').textContent = `${climate_data.precipitation}mm`;
        document.getElementById('soilVal').textContent = `${Math.round(climate_data.soil_moisture * 100)}%`;

        riskBadge.textContent = `VULNERABILITY: ${assessment.risk_level}`;
        riskBadge.className = 'risk-badge ' + assessment.risk_level.toLowerCase();

        if (climate_data.daily_series) {
            try {
                renderTrends(climate_data.daily_series);
            } catch (e) {
                console.error("Chart rendering failed: ", e);
            }
        }
        
        recommendationsList.innerHTML = '';
        if (assessment.recommendations) {
            assessment.recommendations.forEach(rec => {
                const div = document.createElement('div');
                div.className = 'rec-box';
                div.innerHTML = `<i class="fas fa-check-square"></i> <span>${rec}</span>`;
                recommendationsList.appendChild(div);
            });
        }

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
        if (typeof Chart === 'undefined') {
            console.error("Chart.js not loaded.");
            return;
        }
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
        if (locationSelector) locationSelector.classList.add('hidden');
        if (loadingSection) loadingSection.classList.add('hidden');
        if (resultSection) resultSection.classList.add('hidden');
        if (errorSection) errorSection.classList.add('hidden');
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
            const safeName = lastResult.location.name.replace(/[^a-z0-9]/gi, '_');
            a.download = `DroughtSense_Report_${safeName}.pdf`;
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
