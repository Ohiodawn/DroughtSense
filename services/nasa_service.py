import requests
from datetime import datetime, timedelta
from services.location_utils import get_offset_points

def fetch_climate_data(lat, lon, average_radius=False):
    """
    Fetches climate data from NASA POWER API.
    If average_radius is True, fetches 5 points and averages them.
    """
    
    def fetch_point(p_lat, p_lon):
        # Shift back by 3 days to ensure data availability
        end_date = (datetime.now() - timedelta(days=3)).strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=33)).strftime('%Y%m%d')
        
        url = (
            f"https://power.larc.nasa.gov/api/temporal/daily/point?"
            f"parameters=PRECTOTCORR,T2M,GWETROOT&"
            f"community=AG&longitude={p_lon}&latitude={p_lat}&"
            f"start={start_date}&end={end_date}&format=JSON"
        )
        
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            features = data['properties']['parameter']
            
            def get_valid_values(feature_dict):
                return [v for v in feature_dict.values() if v is not None and v > -900]

            temp_vals = get_valid_values(features['T2M'])
            precip_vals = get_valid_values(features['PRECTOTCORR'])
            soil_vals = get_valid_values(features['GWETROOT'])
            
            if not temp_vals or not precip_vals or not soil_vals:
                return None

            return {
                "temperature": sum(temp_vals) / len(temp_vals),
                "precipitation": sum(precip_vals),
                "soil_moisture": sum(soil_vals) / len(soil_vals)
            }
        except Exception as e:
            print(f"NASA API error at ({p_lat}, {p_lon}): {e}")
            return None

    # Determine points to fetch
    points = [(lat, lon)]
    if average_radius:
        points.extend(get_offset_points(lat, lon))

    results = []
    for p_lat, p_lon in points:
        res = fetch_point(p_lat, p_lon)
        if res:
            results.append(res)

    if not results:
        return None

    # Average the results
    avg_temp = sum(r['temperature'] for r in results) / len(results)
    avg_precip = sum(r['precipitation'] for r in results) / len(results)
    avg_soil = sum(r['soil_moisture'] for r in results) / len(results)

    return {
        "temperature": round(avg_temp, 2),
        "precipitation": round(avg_precip, 2),
        "soil_moisture": round(avg_soil, 3),
        "points_averaged": len(results)
    }
