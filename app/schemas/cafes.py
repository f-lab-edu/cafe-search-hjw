# from enum import Enum
from typing import List

from pydantic import BaseModel

from .comments import Comment


class CafeCreate(BaseModel):
    name: str
    address: str
    lat: float
    lon: float
    rep_number: str


class Cafe(CafeCreate):
    comments: List[Comment] = []
    liked_users: List["User"] = []
    facilities: List["Facility"] = []

    class Config:
        orm_mode = True


class FacilityCreate(BaseModel):
    type: str


class Facility(FacilityCreate):
    cafes: List[Cafe] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    type_id: int = 2


class User(UserBase):
    id: int
    is_deleted: bool
    type_id: int
    comments: List[Comment] = []
    liked_cafes: List[Cafe] = []

    class Config:
        orm_mode = True
