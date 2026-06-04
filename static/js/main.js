document.addEventListener('DOMContentLoaded', () => {
    const assessForm = document.getElementById('assessForm');
    const regionInput = document.getElementById('regionInput');
    const submitBtn = document.getElementById('submitBtn');
    
    const loadingSection = document.getElementById('loading');
    const loadingStatus = document.getElementById('loadingStatus');
    const agentLogs = document.getElementById('agentLogs');
    const resultSection = document.getElementById('result');
    const errorSection = document.getElementById('error');

    assessForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        let region = regionInput.value.trim();
        if (!region) return;

        // Basic frontend sanitization
        region = region.replace(/[<>]/g, "").substring(0, 100);
        if (region.length < 2) {
            alert("Please enter a valid region name.");
            return;
        }

        // Reset UI
        resultSection.classList.add('hidden');
        errorSection.classList.add('hidden');
        loadingSection.classList.remove('hidden');
        agentLogs.innerHTML = '';
        loadingStatus.textContent = "Connecting to NASA POWER API...";
        submitBtn.disabled = true;

        try {
            const response = await fetch('/api/assess', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ region })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to generate assessment');
            }

            // Simulate Agent Thinking for UX/Hackathon visibility
            await showAgentLogs(data.agent_logs);

            // Display Results
            displayResults(region, data);

        } catch (err) {
            console.error(err);
            errorSection.querySelector('.error-message').textContent = err.message;
            errorSection.classList.remove('hidden');
        } finally {
            loadingSection.classList.add('hidden');
            submitBtn.disabled = false;
        }
    });

    async function showAgentLogs(logs) {
        for (const log of logs) {
            loadingStatus.textContent = log.status;
            const logEl = document.createElement('div');
            logEl.className = 'log-entry';
            logEl.innerHTML = `> [${log.agent}] ${log.status}`;
            agentLogs.appendChild(logEl);
            // Artificial delay to show the process
            await new Promise(resolve => setTimeout(resolve, 1500));
        }
    }

    function displayResults(region, data) {
        const { climate_data, assessment } = data;
        
        resultRegion.textContent = region;
        explanationText.textContent = assessment.explanation;
        
        // Update Climate Stats
        document.getElementById('tempVal').textContent = climate_data.temperature;
        document.getElementById('precipVal').textContent = climate_data.precipitation;
        document.getElementById('soilVal').textContent = Math.round(climate_data.soil_moisture * 100);

        // Update Risk Badge
        riskBadge.textContent = `${assessment.risk_level} Risk`;
        riskBadge.className = 'badge ' + assessment.risk_level.toLowerCase();
        
        // Inject Recommendations
        recommendationsList.innerHTML = '';
        assessment.recommendations.forEach(rec => {
            const li = document.createElement('li');
            li.innerHTML = `<i class="fas fa-check-circle"></i> ${rec}`;
            recommendationsList.appendChild(li);
        });

        // Handle Citations
        if (assessment.citations && assessment.citations !== "None") {
            citationsText.textContent = assessment.citations;
            citationsSection.classList.remove('hidden');
        } else {
            citationsSection.classList.add('hidden');
        }

        resultSection.classList.remove('hidden');
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }
});
