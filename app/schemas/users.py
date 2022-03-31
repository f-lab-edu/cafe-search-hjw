from enum import Enum, IntEnum

from pydantic import BaseModel


class UserType(IntEnum, Enum):
    ADMIN = 1
    USER = 2


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    type_id: UserType = 2


class Token(BaseModel):
    access_token: str
    token_type: str
