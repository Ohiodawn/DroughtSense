import requests
from datetime import datetime, timedelta
from services.location_utils import get_offset_points

def fetch_climate_data(lat, lon, average_radius=False):
    """
    Fetches climate data from NASA POWER API.
    Returns summarized averages and raw daily series for trends.
    """
    
    def fetch_point(p_lat, p_lon):
        # Shift back by 4 days to ensure data availability (NASA is sometimes delayed)
        end_date = (datetime.now() - timedelta(days=4)).strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=34)).strftime('%Y%m%d')
        
        url = (
            f"https://power.larc.nasa.gov/api/temporal/daily/point?"
            f"parameters=PRECTOTCORR,T2M,GWETROOT&"
            f"community=AG&longitude={p_lon}&latitude={p_lat}&"
            f"start={start_date}&end={end_date}&format=JSON"
        )
        
        try:
            print(f"FETCHING_NASA_DATA: Coords({p_lat}, {p_lon})")
            # Strict timeout to prevent hanging the whole system
            response = requests.get(url, timeout=10) 
            response.raise_for_status()
            data = response.json()
            
            features = data['properties']['parameter']
            
            def get_valid_series(feature_dict):
                return {k: v for k, v in feature_dict.items() if v is not None and v > -900}

            temp_series = get_valid_series(features['T2M'])
            precip_series = get_valid_series(features['PRECTOTCORR'])
            soil_series = get_valid_series(features['GWETROOT'])
            
            if not temp_series or not precip_series or not soil_series:
                print(f"WARN: Incomplete NASA data at ({p_lat}, {p_lon})")
                return None

            return {
                "avg_temp": sum(temp_series.values()) / len(temp_series),
                "total_precip": sum(precip_series.values()),
                "avg_soil": sum(soil_series.values()) / len(soil_series),
                "series": {
                    "dates": list(temp_series.keys()),
                    "temp": list(temp_series.values()),
                    "precip": list(precip_series.values()),
                    "soil": list(soil_series.values())
                }
            }
        except Exception as e:
            print(f"NASA_API_ERROR at ({p_lat}, {p_lon}): {e}")
            return None

    # Determine points to fetch
    points = [(lat, lon)]
    if average_radius:
        # For average_radius, we limit to 3 points total to speed up the process
        offsets = get_offset_points(lat, lon)
        points.extend(offsets[:2]) # Only 2 offsets instead of 4 for performance

    point_results = []
    for p_lat, p_lon in points:
        res = fetch_point(p_lat, p_lon)
        if res:
            point_results.append(res)

    if not point_results:
        print("CRITICAL: No valid NASA data fetched for any point.")
        return None

    # Summarize results
    avg_temp = sum(r['avg_temp'] for r in point_results) / len(point_results)
    avg_precip = sum(r['total_precip'] for r in point_results) / len(point_results)
    avg_soil = sum(r['avg_soil'] for r in point_results) / len(point_results)

    # Use the first successful result for the visual series
    main_series = point_results[0]['series']

    return {
        "temperature": round(avg_temp, 2),
        "precipitation": round(avg_precip, 2),
        "soil_moisture": round(avg_soil, 3),
        "points_averaged": len(point_results),
        "daily_series": main_series
    }
