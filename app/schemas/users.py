# from enum import Enum
# from typing import List

# from pydantic import BaseModel

# from .comments import Comment
# from .cafes import Cafe


# class UserType(int, Enum):
#     admin: 1
#     user: 2


# class UserBase(BaseModel):
#     username: str


# class UserCreate(UserBase):
#     password: str
#     type_id: UserType = 2


# class User(UserBase):
#     id: int
#     is_deleted: bool
#     type_id: int
#     comments: List[Comment] = []
#     liked_cafes: List[Cafe] = []

#     class Config:
#         orm_mode = True
