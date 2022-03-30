from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_session
from schemas.cafes import UserCreate
from services import users


router = APIRouter()


@router.post("/register")
async def register(user: UserCreate, session: Session = Depends(get_session)):
    user_exist = users.check_user_exist(session, username=user.username)
    if user_exist:
        return JSONResponse(
            content=dict(msg="Username Already Exists"), status_code=400
        )
    users.create_user(session, user)
    return JSONResponse(content=dict(msg="User Created Successfully"), status_code=201)
