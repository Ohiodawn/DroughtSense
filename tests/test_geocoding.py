import pytest
import requests_mock
from services.geocoding_service import geocode_region

def test_geocode_success():
    with requests_mock.Mocker() as m:
        m.get('https://nominatim.openstreetmap.org/search?q=Nairobi&format=json&limit=1', json=[
            {'lat': '-1.2833', 'lon': '36.8167'}
        ])
        
        lat, lon = geocode_region('Nairobi')
        assert lat == -1.2833
        assert lon == 36.8167

def test_geocode_not_found():
    with requests_mock.Mocker() as m:
        m.get('https://nominatim.openstreetmap.org/search?q=UnknownPlace&format=json&limit=1', json=[])
        
        lat, lon = geocode_region('UnknownPlace')
        assert lat is None
        assert lon is None

def test_geocode_error():
    with requests_mock.Mocker() as m:
        m.get('https://nominatim.openstreetmap.org/search?q=Nairobi&format=json&limit=1', status_code=500)
        
        lat, lon = geocode_region('Nairobi')
        assert lat is None
        assert lon is None
