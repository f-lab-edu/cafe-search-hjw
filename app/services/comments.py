from sqlalchemy.orm import Session

from schemas.comments import CommentCreate, Comment, CommentBase
from models import models


def create_comment(session: Session, comment: CommentCreate, user_id: int):
    new_comment = models.Comment(
        cafe_id=comment.cafe_id, user_id=user_id, content=comment.content
    )
    session.add(new_comment)
    session.commit()


def check_comment_exist(session: Session, comment_id: int) -> Comment:
    comment = (
        session.query(models.Comment).filter(models.Comment.id == comment_id).first()
    )
    if comment:
        return comment


def delete_comment(session: Session, comment_id: int):
    session.query(models.Comment).filter(models.Comment.id == comment_id).delete()
    session.commit()


def update_comment(session: Session, comment_id: int, comment: CommentBase):
    session.query(models.Comment).filter(models.Comment.id == comment_id).update(
        {"content": comment.content}
    )
    session.commit()
