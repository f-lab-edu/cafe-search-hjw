from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_session
from models import models
from schemas.common import User, LikeBase
from services import likes, cafes
from .users import get_acitve_user

router = APIRouter()


@router.post("")
async def apply_like(
    cafe_id: LikeBase,
    session: Session = Depends(get_session),
    current_user: User = Security(get_acitve_user),
):
    if not cafes.check_cafe_exist_by_id(session, cafe_id.cafe_id):
        raise HTTPException(status_code=404, detail="CAFE_DOES_NOT_EXIST")
    like_obj, flag = likes.get_or_create(
        session, models.Like, cafe_id=cafe_id.cafe_id, user_id=current_user.id
    )
    if flag:
        like_obj.is_deleted = not like_obj.is_deleted
        session.commit()
    return JSONResponse(content=dict(msg="APPLY_SUCCESS"), status_code=201)
