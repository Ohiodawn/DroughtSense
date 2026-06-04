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

def test_assess_endpoint_nairobi(client):
    """Test the assessment endpoint with a real-world city (Nairobi)."""
    # This will trigger real Geocoding and real NASA API calls, but Mock AI
    payload = {"region": "Nairobi"}
    rv = client.post('/api/assess', 
                     data=json.dumps(payload),
                     content_type='application/json')
    
    data = rv.get_json()
    assert rv.status_code == 200
    assert "climate_data" in data
    assert "assessment" in data
    assert data["assessment"]["risk_level"] in ["Low", "Medium", "High", "Critical"]
    assert "Nairobi" in data["assessment"]["explanation"]

def test_assess_endpoint_invalid_region(client):
    """Test the assessment endpoint with an invalid region."""
    payload = {"region": "ThisPlaceDoesNotExist12345"}
    rv = client.post('/api/assess', 
                     data=json.dumps(payload),
                     content_type='application/json')
    
    assert rv.status_code == 404
    assert b"Could not find coordinates" in rv.data

def test_assess_endpoint_empty_payload(client):
    """Test the assessment endpoint with an empty payload."""
    rv = client.post('/api/assess', 
                     data=json.dumps({}),
                     content_type='application/json')
    
    assert rv.status_code == 400
    assert b"Region name is required" in rv.data
