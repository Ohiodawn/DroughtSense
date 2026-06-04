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

from services.geocoding_service import geocode_region
from services.nasa_service import fetch_climate_data
from services.ai_service import AMDInference

def sanitize_region(region):
    """
    Cleans and validates the region input string.
    """
    if not region:
        return None
    cleaned = bleach.clean(region, tags=[], strip=True)
    cleaned = re.sub(r'[^\w\s,\-]', '', cleaned)
    return cleaned.strip()[:100]

@cache.memoize(timeout=86400)
def get_cached_climate(lat, lon, is_large):
    # Rounded to 2 decimals for cache key stability as requested
    r_lat = round(lat, 2)
    r_lon = round(lon, 2)
    return fetch_climate_data(r_lat, r_lon, average_radius=is_large)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/geocode', methods=['POST'])
def geocode():
    """
    New endpoint for the Location Confirmation step.
    Returns up to 3 possible matches.
    """
    data = request.json
    raw_region = data.get('region')
    if not raw_region:
        return jsonify({"error": "Region name is required"}), 400
    
    region = sanitize_region(raw_region)
    if not region or len(region) < 2:
        return jsonify({"error": "Invalid region name"}), 400
        
    matches = geocode_region(region)
    if not matches:
        return jsonify({"error": "We couldn't find that location. Try a more specific name like a province or city."}), 404
        
    return jsonify({"matches": matches})

@app.route('/api/assess', methods=['POST'])
def assess():
    """
    Modified assessment route. Now expects a validated location object.
    """
    data = request.json
    location = data.get('location') # Expects {lat, lon, display_name, is_large, etc}
    
    if not location or 'lat' not in location or 'lon' not in location:
        return jsonify({"error": "Valid location data is required"}), 400
    
    lat = float(location['lat'])
    lon = float(location['lon'])
    is_large = location.get('is_large', False)
    
    # 1. Fetch NASA Data (Cached by coords)
    climate_data = get_cached_climate(lat, lon, is_large)
    if not climate_data:
        return jsonify({"error": "Failed to fetch climate data from NASA POWER API"}), 503
        
    climate_data['region'] = location['display_name']
    
    # 2. Multi-Agent AI Assessment
    result = AMDInference.assess_drought(climate_data)
    
    return jsonify({
        "location": location,
        "climate_data": {
            "temperature": climate_data['temperature'],
            "precipitation": climate_data['precipitation'],
            "soil_moisture": climate_data['soil_moisture'],
            "daily_series": climate_data.get('daily_series')
        },
        "assessment": result['assessment'],
        "agent_logs": result['agent_logs']
    })

if __name__ == '__main__':
    app.run(debug=True)
