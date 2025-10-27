from typing import Tuple

class GeoProviderError(Exception):
    pass


class GeoProvider:
    def __init__(self):
        self.known_cities = {
            "moscow": (55.7558, 37.6176),
            "london": (51.5074, -0.1278),
            "paris": (48.8566, 2.3522),
            "berlin": (52.5200, 13.4050),
            "tver": (56.8587, 35.9176),
            "saint petersburg": (59.9343, 30.3351),
        }

    def get_coords(self, city_name: str) -> Tuple[float, float]:
        key = city_name.lower().strip()
        if key not in self.known_cities:
            raise GeoProviderError(f"Unknown city: {city_name}")
        return self.known_cities[key]
