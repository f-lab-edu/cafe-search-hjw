from datetime import datetime, timedelta

import bcrypt
import jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException
from jwt.exceptions import InvalidSignatureError, DecodeError, ExpiredSignatureError

from models import models
from schemas import users, common
from config import settings


def check_user_exist_by_id(session: Session, user_id: int) -> common.User:
    user = (
        session.query(models.User)
        .filter(models.User.id == user_id, models.User.is_deleted == 0)
        .first()
    )
    if user:
        return user


def check_user_exist_by_name(session: Session, username: str) -> common.User:
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
        username=user.username,
        password=hash_password.decode("utf-8"),
        type_id=user.type_id.value,
    )
    session.add(new_user)
    session.commit()


def delete_user(session: Session, username: str):
    session.query(models.User).filter(models.User.username == username).update(
        {"is_deleted": 1}
    )
    session.commit()


def sign_in(session: Session, username: str, password: str) -> common.User:
    user = check_user_exist_by_name(session, username)
    if not user:
        raise HTTPException(status_code=404, detail="USER_DOES_NOT_EXIST")
    if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return user


def create_token(user: common.User) -> str:
    payload = {
        "user_id": user.id,
        "type_id": user.type_id,
        "exp": datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRATION),
        "scopes": ["admin"] if user.type_id == 1 else [],
    }
    access_token = jwt.encode(
        payload=payload,
        key=settings.TOKEN_SECRET_KEY,
        algorithm=settings.HASHING_ALGORITHM,
    )
    return access_token


def decode_token(token: str) -> common.Payload:
    try:
        decode_token = jwt.decode(
            jwt=token,
            key=settings.TOKEN_SECRET_KEY,
            algorithms=settings.HASHING_ALGORITHM,
        )
        payload = common.Payload(**decode_token)
        return payload

    except InvalidSignatureError:
        raise HTTPException(detail="SIGNATURE_VERIFICATION_FAILED", status_code=400)
    except DecodeError:
        raise HTTPException(detail="DECODE_ERROR", status_code=400)
    except ExpiredSignatureError:
        raise HTTPException(detail="SIGNATURE_EXPIRED", status_code=400)
