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
    Restricts to English (Latin) characters for system stability.
    """
    if not region:
        return None
    cleaned = bleach.clean(region, tags=[], strip=True)
    # Allows only English alphanumeric, spaces, commas, and hyphens
    cleaned = re.sub(r'[^a-zA-Z0-9\s,\-]', '', cleaned)
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
    print(f"API_REQUEST: /api/geocode | Region: {raw_region}")
    
    if not raw_region:
        return jsonify({"error": "Region name is required"}), 400
    
    region = sanitize_region(raw_region)
    if not region or len(region) < 2:
        return jsonify({"error": "Invalid region name"}), 400
        
    matches = geocode_region(region)
    if not matches:
        print(f"API_ERROR: No matches found for {region}")
        return jsonify({"error": "We couldn't find that location. Try a more specific name like a province or city."}), 404
        
    print(f"API_SUCCESS: Found {len(matches)} matches.")
    return jsonify({"matches": matches})

@app.route('/api/assess', methods=['POST'])
def assess():
    """
    Modified assessment route. Now expects a validated location object.
    """
    data = request.json
    location = data.get('location') 
    
    if not location or 'lat' not in location or 'lon' not in location:
        return jsonify({"error": "Valid location data is required"}), 400
    
    print(f"API_REQUEST: /api/assess | Coords: {location['lat']}, {location['lon']}")
    
    lat = float(location['lat'])
    lon = float(location['lon'])
    is_large = location.get('is_large', False)
    
    # 1. Fetch NASA Data (Cached by coords)
    try:
        climate_data = get_cached_climate(lat, lon, is_large)
    except Exception as e:
        print(f"API_ERROR: NASA fetch failed: {e}")
        return jsonify({"error": "NASA Satellite connection timeout."}), 504

    if not climate_data:
        print("API_ERROR: No climate data returned.")
        return jsonify({"error": "Failed to fetch climate data from NASA POWER API"}), 503
        
    climate_data['region'] = location['display_name']
    
    # 2. Multi-Agent AI Assessment
    try:
        result = AMDInference.assess_drought(climate_data)
        print("API_SUCCESS: Assessment generated.")
    except Exception as e:
        print(f"API_ERROR: Inference failed: {e}")
        return jsonify({"error": "AI Inference engine is offline."}), 500
    
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

from services.pdf_service import PDFReportService
from flask import Response

@app.route('/api/report', methods=['POST'])
def download_report():
    """
    Generates and returns a PDF drought report.
    """
    data = request.json
    location = data.get('location')
    climate_data = data.get('climate_data')
    assessment = data.get('assessment')

    if not all([location, climate_data, assessment]):
        return jsonify({"error": "Incomplete data for report generation"}), 400

    pdf_bytes = PDFReportService.generate_report(location, climate_data, assessment)
    
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-disposition": f"attachment; filename=DroughtSense_Report_{location['name'].replace(' ', '_')}.pdf"}
    )

if __name__ == '__main__':
    app.run(debug=True)
