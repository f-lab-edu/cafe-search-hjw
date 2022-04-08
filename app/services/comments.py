from sqlalchemy.orm import Session

from schemas.comments import CommentCreate
from models import models


def create_comment(comment: CommentCreate, user_id: int, session: Session):
    new_comment = models.Comment(
        cafe_id=comment.cafe_id, user_id=user_id, content=comment.content
    )
    session.add(new_comment)
    session.commit()


def delete_comment(session: Session, comment_id: int):
    session.query(models.Comment).filter(models.Comment.id == comment_id).delete()
    