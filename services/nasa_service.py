import requests
from datetime import datetime, timedelta

def fetch_climate_data(lat, lon):
    """
    Fetches climate data from NASA POWER API for the given coordinates.
    Returns a dictionary with summarized values or None.
    """
    # Shift back by 3 days to ensure data availability
    end_date = (datetime.now() - timedelta(days=3)).strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=33)).strftime('%Y%m%d')
    
    url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point?"
        f"parameters=PRECTOTCORR,T2M,GWETROOT&"
        f"community=AG&longitude={lon}&latitude={lat}&"
        f"start={start_date}&end={end_date}&format=JSON"
    )
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Extract features
        features = data['properties']['parameter']
        
        def get_valid_values(feature_dict):
            return [v for v in feature_dict.values() if v is not None and v > -900]

        temp_vals = get_valid_values(features['T2M'])
        precip_vals = get_valid_values(features['PRECTOTCORR'])
        soil_vals = get_valid_values(features['GWETROOT'])
        
        avg_temp = sum(temp_vals) / len(temp_vals) if temp_vals else 0
        total_precip = sum(precip_vals) if precip_vals else 0
        avg_soil_moisture = sum(soil_vals) / len(soil_vals) if soil_vals else 0
        
        return {
            "temperature": round(avg_temp, 2),
            "precipitation": round(total_precip, 2),
            "soil_moisture": round(avg_soil_moisture, 3)
        }
        
    except Exception as e:
        print(f"NASA API error: {e}")
        return None
