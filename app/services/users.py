import bcrypt
import jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException
from jwt.exceptions import InvalidSignatureError, DecodeError

from models import models
from schemas import users, common
from config import settings


def check_user_exist(session: Session, username: str):
    user = (
        session.query(models.User)
        .filter(models.User.username == username, models.User.is_deleted == 0)
        .first()
    )
    if user:
        return user


def create_user(session: Session, user: users.UserCreate):
    hash_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    new_user = models.User(
        username=user.username, password=hash_password, type_id=user.type_id.value
    )
    session.add(new_user)
    session.commit()


def delete_user(session: Session, username: str):
    session.query(models.User).filter(models.User.username == username).update(
        {"is_deleted": 1}
    )
    session.commit()


def sign_in(session: Session, username: str, password: str):
    user = check_user_exist(session, username)
    if not user:
        return False
    if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return user


def create_token(user: common.User):
    payload = {"user_id": str(user.id)}
    access_token = jwt.encode(
        payload=payload,
        key=settings.TOKEN_SECRET_KEY,
        algorithm=settings.HASHING_ALGORITHM,
    )
    return access_token


def check_permission(token: str, user: common.User):
    try:
        decode_token = jwt.decode(
            jwt=token,
            key=settings.TOKEN_SECRET_KEY,
            algorithms=settings.HASHING_ALGORITHM,
        )
        if user.id != decode_token["user_id"]:
            raise HTTPException(status_code=403, detail="UNAUTHORIZED")
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="SIGNATURE_VERIFICATION_FAILED")
    except DecodeError:
        raise HTTPException(status_code=400, detail="DECODE_ERROR")
