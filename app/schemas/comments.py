from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    cafe_id: int


class Comment(CommentBase):
    id: int
    user_id: int
    cafe_id: int

    class Config:
        orm_mode = True
