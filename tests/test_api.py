import json
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test that the homepage loads."""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"DroughtSense AI" in rv.data

def test_geocode_endpoint(client):
    """Test the geocoding endpoint."""
    payload = {"region": "Nairobi"}
    rv = client.post('/api/geocode', 
                     data=json.dumps(payload),
                     content_type='application/json')
    data = rv.get_json()
    assert rv.status_code == 200
    assert "matches" in data
    assert len(data["matches"]) > 0
    assert "Nairobi" in data["matches"][0]["display_name"]

def test_assess_endpoint_with_location(client):
    """Test the assessment endpoint with a resolved location."""
    payload = {
        "location": {
            "name": "Nairobi",
            "display_name": "Nairobi, Kenya",
            "lat": -1.2833,
            "lon": 36.8167,
            "is_large": False
        }
    }
    rv = client.post('/api/assess', 
                     data=json.dumps(payload),
                     content_type='application/json')
    
    data = rv.get_json()
    assert rv.status_code == 200
    assert "climate_data" in data
    assert "assessment" in data
    assert "location" in data

def test_assess_endpoint_missing_location(client):
    """Test the assessment endpoint with missing location data."""
    rv = client.post('/api/assess', 
                     data=json.dumps({}),
                     content_type='application/json')
    
    assert rv.status_code == 400
    assert b"Valid location data is required" in rv.data

def test_report_generation(client):
    """Test the PDF report generation endpoint."""
    payload = {
        "location": {"name": "Nairobi", "display_name": "Nairobi, Kenya", "lat": -1.28, "lon": 36.82},
        "climate_data": {"temperature": 25, "precipitation": 50, "soil_moisture": 0.4},
        "assessment": {
            "risk_level": "Medium",
            "explanation": "Test explanation",
            "recommendations": ["Tip 1", "Tip 2"],
            "citations": "Test Citation"
        }
    }
    rv = client.post('/api/report', 
                     data=json.dumps(payload),
                     content_type='application/json')
    
    assert rv.status_code == 200
    assert rv.mimetype == "application/pdf"
    assert b"%PDF" in rv.data
