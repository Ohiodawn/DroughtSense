from services.geocoding_service import geocode_region
from services.nasa_service import fetch_climate_data

def test_pipeline(region):
    print(f"Testing for: {region}")
    lat, lon = geocode_region(region)
    if lat and lon:
        print(f"Coordinates found: {lat}, {lon}")
        data = fetch_climate_data(lat, lon)
        if data:
            print("Successfully fetched climate data:")
            print(data)
        else:
            print("Failed to fetch climate data.")
    else:
        print("Geocoding failed.")

if __name__ == "__main__":
    test_pipeline("Nairobi")
    print("-" * 20)
    test_pipeline("London")
