# from enum import Enum
from pydantic import BaseModel


class CafeBase(BaseModel):
    name: str
    address: str
    lat: float
    lon: float
    rep_number: str


class FacilityBase(BaseModel):
    type: str
