from fastapi import APIRouter, HTTPException, Depends, Path, Security
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_session
from schemas.comments import CommentCreate, CommentBase
from schemas.common import User
from services import comments, cafes
from .users import get_acitve_user

router = APIRouter()


@router.post("")
async def apply_comment(
    comment: CommentCreate,
    session: Session = Depends(get_session),
    current_user: User = Security(get_acitve_user),
):
    cafe = cafes.check_cafe_exist_by_id(session, comment.cafe_id)
    if not cafe:
        raise HTTPException(status_code=404, detail="CAFE_DOES_NOT_EXIST")
    comments.create_comment(session, comment, current_user.id)
    return JSONResponse(content=dict(msg="CREATE_SUCCESS"), status_code=201)


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int = Path(..., title="The comment id to delete"),
    session: Session = Depends(get_session),
    current_user: User = Security(get_acitve_user),
):
    comment = comments.check_comment_exist(session, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="COMMENT_DOES_NOT_EXIST")
    if current_user.type_id != 1 and comment.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="UNAUTHORIZED")
    comments.delete_comment(session, comment_id)
    return JSONResponse(content=dict(msg="DELETE_SUCCESS"), status_code=201)


@router.patch("/{comment_id}")
async def update_comment(
    comment_info: CommentBase,
    comment_id: int = Path(..., title="The comment id to update"),
    session: Session = Depends(get_session),
    current_user: User = Security(get_acitve_user),
):
    comment = comments.check_comment_exist(session, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="COMMENT_DOES_NOT_EXIST")
    if current_user.type_id != 1 and comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="UNAUTHORIZED")
    comments.update_comment(session, comment_id, comment_info)
    return JSONResponse(content=dict(msg="UPDATE_SUCCESS"), status_code=200)
