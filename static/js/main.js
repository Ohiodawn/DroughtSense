document.addEventListener('DOMContentLoaded', () => {
    const assessForm = document.getElementById('assessForm');
    const regionInput = document.getElementById('regionInput');
    const submitBtn = document.getElementById('submitBtn');
    
    const loadingSection = document.getElementById('loading');
    const resultSection = document.getElementById('result');
    const errorSection = document.getElementById('error');
    
    const resultRegion = document.getElementById('resultRegion');
    const riskBadge = document.getElementById('riskBadge');
    const explanationText = document.getElementById('explanationText');
    const recommendationsList = document.getElementById('recommendationsList');

    assessForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const region = regionInput.value.trim();
        if (!region) return;

        // Reset UI
        resultSection.classList.add('hidden');
        errorSection.classList.add('hidden');
        loadingSection.classList.remove('hidden');
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

        resultSection.classList.remove('hidden');
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }
});
