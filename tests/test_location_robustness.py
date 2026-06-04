import pytest
import json
from app import app
from services.location_utils import clean_query, calculate_centroid, is_large_region, is_valid_coordinate

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_clean_query():
    assert clean_query("  Nairobi, Kenya!  ") == "Nairobi, Kenya"
    # Now correctly handles the space replacement
    assert clean_query("Maharashtra@123") == "Maharashtra 123"

def test_calculate_centroid():
    bbox = ["-1.5", "1.5", "36.5", "37.5"]
    lat, lon = calculate_centroid(bbox)
    assert lat == 0.0
    assert lon == 37.0

def test_is_large_region():
    large_bbox = ["0", "6", "0", "1"] # 6 deg lat span
    small_bbox = ["0", "1", "0", "1"]
    assert is_large_region(large_bbox) is True
    assert is_large_region(small_bbox) is False

def test_is_valid_coordinate():
    assert is_valid_coordinate(15.0, 121.0) is True  # Luzon
    assert is_valid_coordinate(0.0, 0.0) is False    # Null island
    assert is_valid_coordinate(91.0, 0.0) is False   # OOB
    assert is_valid_coordinate(0.0, -150.0) is False # Middle of Pacific Ocean

def test_geocode_endpoint_not_found(client):
    payload = {"region": "SomePlaceThatDefinitelyDoesNotExist123456"}
    rv = client.post('/api/geocode', 
                     data=json.dumps(payload),
                     content_type='application/json')
    assert rv.status_code == 404
    assert b"couldn't find" in rv.data
