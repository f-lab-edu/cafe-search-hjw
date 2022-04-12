from fastapi import APIRouter, HTTPException, Depends, Path, Security
from fastapi.responses import JSONResponse
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from sqlalchemy.orm import Session


from database import get_session
from schemas.users import UserCreate, Token
from schemas.common import User
from services import users

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/signin")


@router.post("/register")
async def register(user: UserCreate, session: Session = Depends(get_session)):
    user_exist = users.check_user_exist_by_name(session, username=user.username)
    if user_exist:
        raise HTTPException(status_code=409, detail="USER_ALREADY_EXIST")
    users.create_user(session, user)
    return JSONResponse(content=dict(msg="CREATE_SUCCESS"), status_code=201)


async def get_acitve_user(
    security_scopes: SecurityScopes,
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    payload = users.decode_token(token)
    user = users.check_user_exist_by_id(session, payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="USER_DOES_NOT_EXIST")
    for scope in security_scopes.scopes:
        if scope not in payload.scopes:
            raise HTTPException(status_code=403, detail="UNAUTHORIZED")
    return user


@router.delete("/{username}")
async def sign_out(
    username: str = Path(..., title="The username of the user to delete"),
    session: Session = Depends(get_session),
    current_user: User = Security(get_acitve_user),
):
    if not users.check_user_exist_by_name(session, username):
        raise HTTPException(status_code=404, detail="USER_DOES_NOT_EXIST")
    if current_user.type_id != 1 and current_user.username != username:
        raise HTTPException(status_code=403, detail="UNAUTHORIZED")
    users.delete_user(session, username)
    return JSONResponse(content=dict(msg="DELETE_SUCCESS"), status_code=201)


@router.post("/signin", response_model=Token)
async def sign_in(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = users.sign_in(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=403, detail="INVALID_PASSWORD")
    access_token = users.create_token(user)
    res = {"access_token": access_token, "token_type": "bearer"}
    return JSONResponse(content=res, status_code=200)
