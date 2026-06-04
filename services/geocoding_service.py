import requests
from services.location_utils import clean_query, calculate_centroid, is_large_region, is_valid_coordinate

def geocode_region(region_name):
    """
    Converts a region name into structured location data using Nominatim.
    Implements multi-stage matching, centroid calculation, and sanity checks.
    """
    cleaned = clean_query(region_name)
    if not cleaned:
        return []

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
        
        # Heuristic: If it's an administrative region, use centroid
        if res.get('type') in ['administrative', 'state', 'province', 'country']:
            centroid = calculate_centroid(bbox)
            if centroid:
                lat, lon = centroid

        # Sanity Check
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
