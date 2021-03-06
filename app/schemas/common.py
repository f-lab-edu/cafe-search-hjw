from typing import List

from pydantic import BaseModel

from .users import UserBase
from .cafes import CafeBase, FacilityBase
from .comments import CommentBase


class User(UserBase):
    id: int
    is_deleted: bool
    type_id: int
    comments: List["Comment"] = []
    liked_cafes: List["Cafe"] = []

    class Config:
        orm_mode = True


class UserInDB(User):
    password: str


class Cafe(CafeBase):
    id: int
    comments: List["Comment"] = []
    liked_users: List["User"] = []
    facilities: List["Facility"] = []

    class Config:
        orm_mode = True


class Comment(CommentBase):
    id: int
    user_id: int
    cafe_id: int

    class Config:
        orm_mode = True


class Facility(FacilityBase):
    cafes: List[Cafe] = []

    class Config:
        orm_mode = True


class Payload(BaseModel):
    user_id: int
    type_id: int
    exp: int
    scopes: List[str]
