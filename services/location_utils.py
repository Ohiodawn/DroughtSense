import re

def clean_query(query):
    """
    Strips special characters and extra whitespace from the user input.
    Enforces English-only (Latin) characters to ensure compatibility.
    """
    if not query:
        return ""
    # Remove non-English (Latin) characters and non-standard symbols
    # Allows: a-z, A-Z, 0-9, space, comma, hyphen
    cleaned = re.sub(r'[^a-zA-Z0-9\s,\-]', ' ', query)
    # Collapse multiple spaces and trim
    return " ".join(cleaned.split())

def calculate_centroid(boundingbox):
    """
    Calculates the center point of a bounding box.
    Nominatim boundingbox: [south, north, west, east]
    Returns (lat, lon)
    """
    if not boundingbox or len(boundingbox) != 4:
        return None
    
    bbox = [float(x) for x in boundingbox]
    lat = (bbox[0] + bbox[1]) / 2
    lon = (bbox[2] + bbox[3]) / 2
    return round(lat, 4), round(lon, 4)

def is_large_region(boundingbox):
    """
    Determines if a region is 'large' based on its bounding box span (> 5 degrees).
    """
    if not boundingbox or len(boundingbox) != 4:
        return False
    
    bbox = [float(x) for x in boundingbox]
    lat_span = abs(bbox[1] - bbox[0])
    lon_span = abs(bbox[3] - bbox[2])
    
    return lat_span > 5.0 or lon_span > 5.0

def is_valid_coordinate(lat, lon):
    """
    Performs sanity checks on coordinates.
    """
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        return False
    
    if abs(lat) < 0.001 and abs(lon) < 0.001:
        return False # Reject (0,0)

    # Simple bounding boxes for major ocean zones
    ocean_zones = [
        (-60, 60, -180, -100), # Central Pacific
        (-60, 60, -60, -20),   # Central Atlantic
        (-60, 20, 50, 100),    # Indian Ocean
        (60, 90, -180, 180),   # Arctic
        (-90, -60, -180, 180), # Southern Ocean
    ]

    for lat_min, lat_max, lon_min, lon_max in ocean_zones:
        if lat_min < lat < lat_max and lon_min < lon < lon_max:
            return False

    return True

def get_offset_points(lat, lon, offset=0.5):
    """
    Generates 4 surrounding points (N, S, E, W) for radius averaging.
    """
    return [
        (lat + offset, lon),
        (lat - offset, lon),
        (lat, lon + offset),
        (lat, lon - offset)
    ]
