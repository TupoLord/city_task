from fastapi import FastAPI, HTTPException, Query
from typing import List
from .models import City, CityCreateRequest, NearestCity
from .storage import CityStorage
from .provider import GeoProvider, GeoProviderError
from .distance import sort_cities_by_distance

app = FastAPI(
    title="City API",
    description="Тестовое API для управления городами и поиска ближайших",
    version="1.0.0",
)

storage = CityStorage()
geo = GeoProvider()

@app.post("/cities", response_model=City, status_code=201)
def add_city(req: CityCreateRequest):
    try:
        lat, lon = geo.get_coords(req.name)
    except GeoProviderError as e:
        raise HTTPException(status_code=404, detail=str(e))
    try:
        city = storage.add_city(req.name, lat, lon)
    except ValueError:
        raise HTTPException(status_code=409, detail="City already exists")
    return city


@app.get("/cities", response_model=List[City])
def list_cities():
    return storage.list_cities()


@app.get("/cities/{city_id}", response_model=City)
def get_city(city_id: int):
    city = storage.get_by_id(city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.delete("/cities/{city_id}", status_code=204)
def delete_city(city_id: int):
    ok = storage.delete_city(city_id)
    if not ok:
        raise HTTPException(status_code=404, detail="City not found")
    return


@app.get("/nearest", response_model=List[NearestCity])
def get_nearest(
    lat: float = Query(..., ge=-90.0, le=90.0),
    lon: float = Query(..., ge=-180.0, le=180.0),
    k: int = Query(2, ge=1, le=10),
):
    cities = storage.list_cities()
    if not cities:
        return []

    ranked = sort_cities_by_distance(lat, lon, cities)
    topk = ranked[:k]

    result = [
        NearestCity(
            city=city,
            distance_km=round(dist, 3)
        )
        for dist, city in topk
    ]
    return result
