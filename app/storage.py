from typing import Dict, List, Optional
from .models import City

class CityStorage:

    def __init__(self):
        self._cities: Dict[int, City] = {}
        self._next_id: int = 1

    def list_cities(self) -> List[City]:
        return list(self._cities.values())

    def get_by_id(self, city_id: int) -> Optional[City]:
        return self._cities.get(city_id)

    def get_by_name_casefold(self, name: str) -> Optional[City]:
        name_cf = name.casefold()
        for c in self._cities.values():
            if c.name.casefold() == name_cf:
                return c
        return None

    def add_city(self, name: str, lat: float, lon: float) -> City:
        existing = self.get_by_name_casefold(name)
        if existing:
            raise ValueError("City already exists")

        new_city = City(
            id=self._next_id,
            name=name,
            lat=lat,
            lon=lon,
        )
        self._cities[self._next_id] = new_city
        self._next_id += 1
        return new_city

    def delete_city(self, city_id: int) -> bool:
        if city_id in self._cities:
            del self._cities[city_id]
            return True
        return False
