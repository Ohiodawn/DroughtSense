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

    // Premium Map Style (Voyager by CARTO)
    function initMap() {
        if (map) return;
        map = L.map('map', {
            zoomControl: false,
            scrollWheelZoom: false,
            dragging: !L.Browser.mobile
        }).setView([0, 0], 2);
        
        L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OSM</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 20
        }).addTo(map);

        L.control.zoom({ position: 'bottomright' }).addTo(map);
    }

    function updateMap(lat, lon, name) {
        initMap();
        const coords = [lat, lon];
        map.setView(coords, 11); // Closer zoom for hyper-local feel
        
        if (marker) {
            marker.setLatLng(coords).setPopupContent(`<b>${name}</b>`);
        } else {
            marker = L.marker(coords).addTo(map).bindPopup(`<b>${name}</b>`).openPopup();
        }
        
        setTimeout(() => map.invalidateSize(), 300);
    }

    // Handle Search
    assessForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const region = regionInput.value.trim();
        if (!region) return;

        // English-only validation
        const englishOnly = region.replace(/[^a-zA-Z0-9\s,\-]/g, "");
        if (englishOnly.length !== region.length || region.length < 2) {
            showError("Please use English characters (min 2 characters).");
            return;
        }

        hideAll();
        loadingSection.classList.remove('hidden');
        loadingStatus.textContent = "Acquiring Geospatial Context...";
        agentLogs.innerHTML = '';
        submitBtn.disabled = true;

        try {
            const response = await fetch('/api/geocode', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ region })
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Geocoding failed');

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
            div.className = 'match-item-new';
            div.innerHTML = `
                <div>
                    <strong style="color: var(--forest-dark); font-size: 1.1rem;">${match.display_name}</strong><br>
                    <small style="color: var(--text-muted); text-transform: uppercase; font-weight: 700; font-size: 0.7rem;">${match.type} • ${match.lat.toFixed(2)}°N, ${match.lon.toFixed(2)}°E</small>
                </div>
                <i class="fas fa-arrow-right" style="color: var(--primary); font-size: 1.2rem;"></i>
            `;
            div.onclick = () => runAssessment(match);
            matchList.appendChild(div);
        });
        locationSelector.classList.remove('hidden');
    }

    async function runAssessment(location) {
        hideAll();
        loadingSection.classList.remove('hidden');
        loadingStatus.textContent = "Interrogating NASA Satellite Networks...";
        submitBtn.disabled = true;

        try {
            const response = await fetch('/api/assess', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ location })
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Assessment failed');

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
            logEl.innerHTML = `<span style="color: var(--accent)">➔</span> [${log.agent}] ${log.status}`;
            agentLogs.appendChild(logEl);
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }

    function displayResults(data) {
        lastResult = data;
        const { location, climate_data, assessment } = data;
        
        resolvedLocation.textContent = location.display_name;
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

        riskBadge.textContent = `${assessment.risk_level} Risk`;
        riskBadge.className = 'risk-badge-lg ' + assessment.risk_level.toLowerCase();

        if (climate_data.daily_series) renderTrends(climate_data.daily_series);
        
        recommendationsList.innerHTML = '';
        assessment.recommendations.forEach(rec => {
            const li = document.createElement('li');
            li.className = 'rec-item';
            li.innerHTML = `<i class="fas fa-check-circle"></i> <span>${rec}</span>`;
            recommendationsList.appendChild(li);
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
                        label: 'Rainfall (mm)',
                        data: series.precip,
                        borderColor: '#1b5e20',
                        backgroundColor: 'rgba(27, 94, 32, 0.05)',
                        borderWidth: 4,
                        yAxisID: 'y',
                        fill: true,
                        pointRadius: 0,
                        tension: 0.4
                    },
                    {
                        label: 'Temp (°C)',
                        data: series.temp,
                        borderColor: '#e74c3c',
                        borderWidth: 4,
                        yAxisID: 'y1',
                        pointRadius: 0,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: { mode: 'index', intersect: false },
                scales: {
                    x: { grid: { display: false }, ticks: { font: { weight: '600' } } },
                    y: { type: 'linear', display: true, position: 'left', title: { display: true, text: 'Rainfall (mm)', font: { weight: '800' } } },
                    y1: { type: 'linear', display: true, position: 'right', grid: { drawOnChartArea: false }, title: { display: true, text: 'Temp (°C)', font: { weight: '800' } } }
                },
                plugins: { legend: { position: 'top', labels: { font: { weight: '700' }, usePointStyle: true, boxWidth: 8 } } }
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
        downloadPdfBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Processing...';

        try {
            const response = await fetch('/api/report', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(lastResult)
            });
            if (!response.ok) throw new Error('Failed to generate PDF');
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `DroughtSense_Report_${lastResult.location.name}.pdf`;
            document.body.appendChild(a);
            a.click();
            a.remove();
        } catch (err) {
            alert("Error downloading PDF: " + err.message);
        } finally {
            downloadPdfBtn.disabled = false;
            downloadPdfBtn.innerHTML = originalText;
        }
    });
});
