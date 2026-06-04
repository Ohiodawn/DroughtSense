import pytest
import requests_mock
from services.geocoding_service import geocode_region

def test_geocode_success():
    with requests_mock.Mocker() as m:
        # Mocking the new URL format with addressdetails=1 and limit=3
        m.get('https://nominatim.openstreetmap.org/search?q=Nairobi&format=json&limit=3&addressdetails=1', json=[
            {
                'lat': '-1.2833', 
                'lon': '36.8167', 
                'display_name': 'Nairobi, Kenya',
                'type': 'city',
                'address': {'city': 'Nairobi', 'country': 'Kenya'},
                'importance': 0.9
            }
        ])
        
        results = geocode_region('Nairobi')
        assert len(results) == 1
        assert results[0]['lat'] == -1.2833
        assert results[0]['lon'] == 36.8167
        assert results[0]['name'] == 'Nairobi'

def test_geocode_not_found():
    with requests_mock.Mocker() as m:
        m.get('https://nominatim.openstreetmap.org/search?q=UnknownPlace&format=json&limit=3&addressdetails=1', json=[])
        m.get('https://nominatim.openstreetmap.org/search?q=UnknownPlace%20agricultural%20region&format=json&limit=3&addressdetails=1', json=[])
        
        results = geocode_region('UnknownPlace')
        assert len(results) == 0

def test_geocode_error():
    with requests_mock.Mocker() as m:
        m.get('https://nominatim.openstreetmap.org/search?q=Nairobi&format=json&limit=3&addressdetails=1', status_code=500)
        m.get('https://nominatim.openstreetmap.org/search?q=Nairobi%20agricultural%20region&format=json&limit=3&addressdetails=1', status_code=500)
        
        results = geocode_region('Nairobi')
        assert len(results) == 0
