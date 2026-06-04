import pytest
import requests_mock
from services.nasa_service import fetch_climate_data

def test_fetch_climate_success():
    with requests_mock.Mocker() as m:
        # Mocking the NASA POWER API URL (ignoring specific dates for simplicity)
        m.get('https://power.larc.nasa.gov/api/temporal/daily/point', json={
            'properties': {
                'parameter': {
                    'T2M': {'20260101': 25.0, '20260102': 27.0},
                    'PRECTOTCORR': {'20260101': 10.0, '20260102': 5.0},
                    'GWETROOT': {'20260101': 0.5, '20260102': 0.4}
                }
            }
        })
        
        data = fetch_climate_data(-1.2833, 36.8167)
        assert data['temperature'] == 26.0
        assert data['precipitation'] == 15.0
        assert data['soil_moisture'] == 0.45

def test_fetch_climate_invalid_data():
    with requests_mock.Mocker() as m:
        m.get('https://power.larc.nasa.gov/api/temporal/daily/point', json={
            'properties': {
                'parameter': {
                    'T2M': {'20260101': -999, '20260102': 25.0},
                    'PRECTOTCORR': {'20260101': -999, '20260102': 10.0},
                    'GWETROOT': {'20260101': -999, '20260102': 0.5}
                }
            }
        })
        
        data = fetch_climate_data(-1.2833, 36.8167)
        # Should filter out -999
        assert data['temperature'] == 25.0
        assert data['precipitation'] == 10.0
        assert data['soil_moisture'] == 0.5

def test_fetch_climate_error():
    with requests_mock.Mocker() as m:
        m.get('https://power.larc.nasa.gov/api/temporal/daily/point', status_code=500)
        
        data = fetch_climate_data(-1.2833, 36.8167)
        assert data is None
