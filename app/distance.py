import math
from .models import City

EARTH_RADIUS_KM = 6371.0


def haversine_distance_km(lat1: float, lon1: float,
                          lat2: float, lon2: float) -> float:

    rlat1 = math.radians(lat1)
    rlon1 = math.radians(lon1)
    rlat2 = math.radians(lat2)
    rlon2 = math.radians(lon2)

    dlat = rlat2 - rlat1
    dlon = rlon2 - rlon1

    a = (math.sin(dlat / 2) ** 2
         + math.cos(rlat1) * math.cos(rlat2) * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS_KM * c


def sort_cities_by_distance(lat: float, lon: float, cities: list[City]):
    out = []
    for city in cities:
        dist = haversine_distance_km(lat, lon, city.lat, city.lon)
        out.append((dist, city))
    out.sort(key=lambda x: x[0])
    return out
