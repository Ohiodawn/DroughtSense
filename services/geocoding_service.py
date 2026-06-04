import requests
import os
import googlemaps
from services.location_utils import clean_query, calculate_centroid, is_large_region, is_valid_coordinate

def geocode_region(region_name):
    """
    Orchestrates geocoding by prioritizing Google Maps (if key available)
    and falling back to a robust Nominatim pipeline.
    """
    cleaned = clean_query(region_name)
    if not cleaned:
        return []

    google_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if google_key:
        print(f"Using Google Maps for geocoding: {cleaned}")
        results = google_geocode(cleaned, google_key)
        if results:
            return results
    
    print(f"Using Nominatim for geocoding: {cleaned}")
    return nominatim_geocode(cleaned)

def google_geocode(query, api_key):
    """
    Geocodes using Google Maps API.
    """
    try:
        gmaps = googlemaps.Client(key=api_key)
        geocode_result = gmaps.geocode(query)
        
        processed = []
        for res in geocode_result[:3]:
            lat = res['geometry']['location']['lat']
            lon = res['geometry']['location']['lng']
            
            # Determine if large region using viewport span
            viewport = res['geometry'].get('viewport', {})
            is_large = False
            if viewport:
                lat_span = abs(viewport['northeast']['lat'] - viewport['southwest']['lat'])
                lon_span = abs(viewport['northeast']['lng'] - viewport['southwest']['lng'])
                is_large = lat_span > 5.0 or lon_span > 5.0

            # Extract simple name
            name = res['address_components'][0]['long_name']
            country = next((c['long_name'] for c in res['address_components'] if 'country' in c['types']), "Unknown")

            processed.append({
                "display_name": res['formatted_address'],
                "name": name,
                "country": country,
                "type": ", ".join(res['types']),
                "lat": lat,
                "lon": lon,
                "is_large": is_large,
                "importance": 1.0 # Google is high confidence
            })
        return processed
    except Exception as e:
        print(f"Google Maps API error: {e}")
        return []

def nominatim_geocode(cleaned):
    """
    Original robust Nominatim pipeline.
    """
    def call_nominatim(q):
        url = f"https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=3&addressdetails=1"
        headers = {'User-Agent': 'DroughtSenseAI/2.0 (hackathon project)'}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Nominatim API error for query '{q}': {e}")
            return []

    # Stage 1: Exact Cleaned Query
    results = call_nominatim(cleaned)

    # Stage 2: Country Bias Check (if single word)
    if not results and " " not in cleaned:
        results = call_nominatim(f"{cleaned} agricultural region")

    # Stage 3: Fuzzy Fallback (remove last word)
    if not results and " " in cleaned:
        parts = cleaned.split()
        fuzzy_query = " ".join(parts[:-1])
        results = call_nominatim(fuzzy_query)

    processed_results = []
    for res in results:
        lat = float(res['lat'])
        lon = float(res['lon'])
        bbox = res.get('boundingbox')
        
        if res.get('type') in ['administrative', 'state', 'province', 'country']:
            centroid = calculate_centroid(bbox)
            if centroid:
                lat, lon = centroid

        if not is_valid_coordinate(lat, lon):
            continue

        processed_results.append({
            "display_name": res['display_name'],
            "name": res.get('address', {}).get('city') or res.get('address', {}).get('state') or res.get('name'),
            "country": res.get('address', {}).get('country'),
            "type": res.get('type'),
            "lat": lat,
            "lon": lon,
            "is_large": is_large_region(bbox),
            "importance": res.get('importance', 0)
        })

    return processed_results
