from typing import Optional

from pydantic import BaseModel


class CafeBase(BaseModel):
    name: str
    address: str
    lat: float
    lon: float
    rep_number: str


class CafeUpdate(BaseModel):
    name: Optional[str]
    address: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    rep_number: Optional[str]


class FacilityBase(BaseModel):
    type: str
