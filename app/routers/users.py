from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Path, Header
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from database import get_session
from schemas.users import UserCreate, Token
from services import users

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/signin")


@router.post("/register")
async def register(user: UserCreate, session: Session = Depends(get_session)):
    try:
        user_exist = users.check_user_exist(session, username=user.username)
        if user_exist:
            raise HTTPException(status_code=409, detail="USER_ALREADY_EXIST")
        users.create_user(session, user)
        return JSONResponse(content=dict(msg="CREATE_SUCCESS"), status_code=201)

    except HTTPException as e:
        return JSONResponse(content=dict(msg=e.detail), status_code=e.status_code)


@router.delete("/{username}", dependencies=[Depends(oauth2_scheme)])
async def sign_out(
    username: str = Path(..., title="The username of the user to delete"),
    session: Session = Depends(get_session),
    authorization: Optional[str] = Header(None),
):
    try:
        user = users.check_user_exist(session, username=username)
        if not user:
            raise HTTPException(status_code=404, detail="USER_DOES_NOT_EXIST")
        payload = users.decode_token(authorization)
        if int(payload.type_id) != 1 and user.username != payload.username:
            raise HTTPException(status_code=403, detail="UNAUTHORIZED")
        users.delete_user(session, username)
        return JSONResponse(content=dict(msg="DELETE_SUCCESS"), status_code=201)

    except HTTPException as e:
        return JSONResponse(content=dict(msg=e.detail), status_code=e.status_code)


@router.post("/signin", response_model=Token)
async def sign_in(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    try:
        user = users.sign_in(session, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=403, detail="INVALID_PASSWORD")
        access_token = users.create_token(user)
        res = {"access_token": access_token, "token_type": "bearer"}
        return JSONResponse(content=res, status_code=200)

    except HTTPException as e:
        return JSONResponse(content=dict(msg=e.detail), status_code=e.status_code)
