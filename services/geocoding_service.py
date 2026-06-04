import requests

def geocode_region(region_name):
    """
    Converts a region name into Latitude and Longitude using Nominatim (OSM).
    Returns (lat, lon) or (None, None) if not found.
    """
    url = f"https://nominatim.openstreetmap.org/search?q={region_name}&format=json&limit=1"
    headers = {
        'User-Agent': 'DroughtSenseAI/1.0 (hackathon project)'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
        return None, None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None, None
