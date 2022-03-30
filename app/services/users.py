import bcrypt
from sqlalchemy.orm import Session

from models import models
from schemas import cafes


def check_user_exist(session: Session, username):
    user = session.query(models.User).filter(models.User.username == username).first()
    if user:
        return True
    else:
        return False


def create_user(session: Session, user: cafes.UserCreate):
    hash_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    new_user = models.User(
        username=user.username, password=hash_password, type_id=user.type_id
    )
    session.add(new_user)
    session.commit()
