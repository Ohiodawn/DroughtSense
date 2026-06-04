document.addEventListener('DOMContentLoaded', () => {
    const assessForm = document.getElementById('assessForm');
    const regionInput = document.getElementById('regionInput');
    const submitBtn = document.getElementById('submitBtn');
    
    const alertContainer = document.getElementById('alertContainer');
    const progressBar = document.getElementById('progressBar');
    const progressFill = document.getElementById('progressFill');

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
    
    const soilFill = document.getElementById('soilFill');
    const errorSection = document.getElementById('error');

    let trendsChart = null;
    let map = null;
    let marker = null;
    let lastResult = null;

    // Use ResizeObserver to prevent Leaflet grey-box bugs
    const resizeObserver = new ResizeObserver(() => {
        if (map) map.invalidateSize();
    });

    function initMap() {
        if (map) return;
        const mapContainer = document.getElementById('map');
        if (!mapContainer) return;

        map = L.map('map', {
            zoomControl: true,
            scrollWheelZoom: false
        }).setView([0, 0], 2);
        
        L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; OSM contributors',
            maxZoom: 20
        }).addTo(map);

        resizeObserver.observe(mapContainer);
    }

    function updateMap(lat, lon, name, isLarge) {
        initMap();
        const coords = [lat, lon];
        const zoom = isLarge ? 6 : 10;
        map.setView(coords, zoom);
        
        if (marker) {
            marker.setLatLng(coords).setPopupContent(name);
        } else {
            marker = L.marker(coords).addTo(map).bindPopup(name).openPopup();
        }
    }

    function setProgress(percent) {
        progressBar.style.display = 'block';
        progressFill.style.width = percent + '%';
        if (percent >= 100) {
            setTimeout(() => {
                progressBar.style.display = 'none';
                progressFill.style.width = '0%';
            }, 1000);
        }
    }

    function showAlert(msg) {
        alertContainer.innerHTML = `
            <div class="system-alert">
                <i class="fas fa-triangle-exclamation"></i>
                <span>${msg}</span>
            </div>
        `;
        alertContainer.classList.remove('hidden');
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    assessForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const region = regionInput.value.trim();
        if (!region) return;

        // Validation
        const englishOnly = region.replace(/[^a-zA-Z0-9\s,\-]/g, "");
        if (englishOnly.length !== region.length || region.length < 2) {
            showAlert("Input Protocol Violation: Use English (Latin) characters only.");
            return;
        }

        hideAll();
        loadingSection.classList.remove('hidden');
        loadingStatus.textContent = "PROTOCOL: REGION_RESOLVE...";
        agentLogs.innerHTML = '';
        setProgress(20);
        
        // Lock UI
        submitBtn.disabled = true;
        regionInput.disabled = true;

        try {
            const response = await fetch('/api/geocode', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ region })
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'RESOLUTION_FAILED');

            setProgress(40);
            if (data.matches.length === 1) {
                runAssessment(data.matches[0]);
            } else {
                showLocationSelector(data.matches);
            }
        } catch (err) {
            showError(err.message);
        } finally {
            submitBtn.disabled = false;
            regionInput.disabled = false;
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
                    <small style="color: #666; font-family: var(--font-mono)">${match.lat.toFixed(4)}, ${match.lon.toFixed(4)}</small>
                </div>
                <i class="fas fa-chevron-right" style="color: var(--primary)"></i>
            `;
            div.onclick = () => runAssessment(match);
            matchList.appendChild(div);
        });
        locationSelector.classList.remove('hidden');
        setProgress(50);
    }

    async function runAssessment(location) {
        hideAll();
        loadingSection.classList.remove('hidden');
        loadingStatus.textContent = "PROTOCOL: SENSOR_INTERROGATION...";
        setProgress(60);

        try {
            const response = await fetch('/api/assess', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ location })
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'ANALYSIS_FAILED');

            lastResult = data;
            setProgress(80);
            await showAgentLogs(data.agent_logs);
            displayResults(data);
            setProgress(100);

        } catch (err) {
            showError(err.message);
        }
    }

    async function showAgentLogs(logs) {
        if (!logs) return;
        agentLogs.innerHTML = '';
        for (const log of logs) {
            const logEl = document.createElement('div');
            logEl.style.marginBottom = "4px";
            logEl.innerHTML = `<span style="color: var(--accent)">></span> [${log.agent.toUpperCase()}] ${log.status}`;
            agentLogs.appendChild(logEl);
            agentLogs.scrollTop = agentLogs.scrollHeight;
            await new Promise(resolve => setTimeout(resolve, 800));
        }
    }

    function displayResults(data) {
        const { location, climate_data, assessment } = data;
        
        resolvedLocation.textContent = `SYSTEM_ID: ${location.display_name}`;
        largeRegionWarning.classList.toggle('hidden', !location.is_large);

        updateMap(location.lat, location.lon, location.name, location.is_large);

        resultRegion.textContent = location.name;
        explanationText.textContent = assessment.explanation;
        
        document.getElementById('tempVal').textContent = `${climate_data.temperature}°C`;
        document.getElementById('precipVal').textContent = `${climate_data.precipitation}mm`;
        document.getElementById('soilVal').textContent = `${Math.round(climate_data.soil_moisture * 100)}%`;
        
        // Update Soil Gauge
        soilFill.style.width = (climate_data.soil_moisture * 100) + '%';

        riskBadge.textContent = assessment.risk_level;
        riskBadge.className = 'risk-level-badge ' + assessment.risk_level.toLowerCase();

        if (climate_data.daily_series) renderTrends(climate_data.daily_series);
        
        recommendationsList.innerHTML = '';
        assessment.recommendations.forEach(rec => {
            const div = document.createElement('div');
            div.className = 'rec-card';
            div.innerHTML = `<i class="fas fa-check-square"></i> <p>${rec}</p>`;
            recommendationsList.appendChild(div);
        });

        citationsText.textContent = assessment.citations;
        citationsSection.classList.toggle('hidden', !assessment.citations || assessment.citations === "None");

        resultSection.classList.remove('hidden');
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }

    function renderTrends(series) {
        const ctx = document.getElementById('trendsChart').getContext('2d');
        if (trendsChart) trendsChart.destroy();

        trendsChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: series.dates.map(d => `${d.substring(4,6)}/${d.substring(6,8)}`),
                datasets: [
                    {
                        label: 'Rainfall (mm)',
                        data: series.precip,
                        borderColor: '#2e7d32',
                        backgroundColor: 'rgba(46, 125, 50, 0.05)',
                        borderWidth: 3,
                        yAxisID: 'y',
                        fill: true,
                        pointRadius: 0,
                        tension: 0.2
                    },
                    {
                        label: 'Temp (°C)',
                        data: series.temp,
                        borderColor: '#c0392b',
                        borderWidth: 3,
                        yAxisID: 'y1',
                        pointRadius: 0,
                        tension: 0.2
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: 'index', intersect: false },
                scales: {
                    x: { grid: { display: false } },
                    y: { type: 'linear', position: 'left', title: { display: true, text: 'Rainfall (mm)' } },
                    y1: { type: 'linear', position: 'right', grid: { display: false }, title: { display: true, text: 'Temp (°C)' } }
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
        [locationSelector, loadingSection, resultSection, errorSection, alertContainer].forEach(el => {
            if (el) el.classList.add('hidden');
        });
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
            a.download = `DroughtSense_Report_${lastResult.location.name.replace(/[^a-z0-9]/gi, '_')}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
        } catch (err) {
            showAlert("Export Error: " + err.message);
        } finally {
            downloadPdfBtn.disabled = false;
            downloadPdfBtn.innerHTML = originalText;
        }
    });
});
