from fastapi import APIRouter, HTTPException, Depends, Path
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_session
from schemas.users import UserCreate, Token
from services import users

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/sign_in")


@router.post("/register")
async def register(user: UserCreate, session: Session = Depends(get_session)):
    user_exist = users.check_user_exist(session, username=user.username)
    if user_exist:
        raise HTTPException(status_code=409, detail="USER_ALREADY_EXIST")
    users.create_user(session, user)
    return JSONResponse(content=dict(msg="CREATE_SUCCESS"), status_code=201)


@router.delete(
    "/{username}",
    dependencies=[Depends(oauth2_scheme), Depends(users.check_permission)],
)
async def sign_out(
    username: str = Path(..., title="The username of the user to delete"),
    session: Session = Depends(get_session),
):
    if not users.check_user_exist(session, username=username):
        raise HTTPException(status_code=404, detail="USER_DOES_NOT_EXIST")
    users.delete_user(session, username)
    return JSONResponse(content=dict(msg="DELETE_SUCCESS"), status_code=201)


@router.post("/sign_in", response_model=Token)
async def sign_in(
    session: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = users.sign_in(session, form_data.username, form_data.password)
    access_token = users.create_token(user)
    return {"access_token": access_token, "token_type": "bearer"}
