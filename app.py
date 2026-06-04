import os
import json
import bleach
import re
from flask import Flask, request, jsonify, render_template
from flask_caching import Cache
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-123')

# Cache configuration
app.config['CACHE_TYPE'] = 'FileSystemCache'
app.config['CACHE_DIR'] = 'cache-dir'
app.config['CACHE_DEFAULT_TIMEOUT'] = 86400  # 24 hours
cache = Cache(app)

@app.route('/')
def index():
    return render_template('index.html')

from services.geocoding_service import geocode_region
from services.nasa_service import fetch_climate_data
from services.ai_service import AMDInference

@cache.memoize(timeout=604800)  # Cache geocoding for 1 week
def get_cached_coordinates(region):
    return geocode_region(region)

@cache.memoize(timeout=86400)  # Cache climate data for 24 hours
def get_cached_climate(lat, lon):
    return fetch_climate_data(lat, lon)

def sanitize_region(region):
    """
    Cleans and validates the region input string.
    """
    if not region:
        return None
    # Strip HTML tags
    cleaned = bleach.clean(region, tags=[], strip=True)
    # Remove any characters that aren't alphanumeric, spaces, commas, or hyphens
    cleaned = re.sub(r'[^\w\s,\-]', '', cleaned)
    # Limit length
    return cleaned.strip()[:100]

@app.route('/api/assess', methods=['POST'])
def assess():
    data = request.json
    raw_region = data.get('region')
    
    if not raw_region:
        return jsonify({"error": "Region name is required"}), 400

    region = sanitize_region(raw_region)
    if not region or len(region) < 2:
        return jsonify({"error": "Invalid region name provided"}), 400
    
    # 1. Geocode (Cached)
    lat, lon = get_cached_coordinates(region)
    if not lat or not lon:
        return jsonify({"error": f"Could not find coordinates for region: {region}"}), 404
        
    # 2. Fetch NASA Data (Cached)
    climate_data = get_cached_climate(lat, lon)
    if not climate_data:
        return jsonify({"error": "Failed to fetch climate data from NASA POWER API"}), 503
        
    # Add region name for the AI context
    climate_data['region'] = region
    
    # 3. Use AI (Phase 5: Real AMD Inference if configured)
    # The result now comes from the Multi-Agent Orchestrator
    result = AMDInference.assess_drought(climate_data)
    
    # Return climate data, assessment, and agent reports for UI visibility
    return jsonify({
        "climate_data": {
            "temperature": climate_data['temperature'],
            "precipitation": climate_data['precipitation'],
            "soil_moisture": climate_data['soil_moisture']
        },
        "assessment": result['assessment'],
        "agent_logs": result['agent_logs']
    })

if __name__ == '__main__':
    app.run(debug=True)
