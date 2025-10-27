from pydantic import BaseModel, Field


class CityCreateRequest(BaseModel):
    name: str = Field(..., min_length=1)


class City(BaseModel):
    id: int
    name: str
    lat: float
    lon: float


class NearestCity(BaseModel):
    city: City
    distance_km: float
