from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Path, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session


from database import get_session
from schemas.comments import CommentCreate, CommentBase
from services import users, comments, cafes
from .users import oauth2_scheme

router = APIRouter()


@router.post("", dependencies=[Depends(oauth2_scheme)])
async def apply_comment(
    comment: CommentCreate,
    session: Session = Depends(get_session),
    authorization: Optional[str] = Header(None),
):
    try:
        payload = users.decode_token(authorization)
        cafe = cafes.check_cafe_exist(session, comment.cafe_id)
        if not cafe:
            raise HTTPException(status_code=404, detail="CAFE_DOES_NOT_EXIST")
        comments.create_comment(session, comment, payload.user_id)
        return JSONResponse(content=dict(msg="CREATE_SUCCESS"), status_code=201)

    except HTTPException as e:
        return JSONResponse(content=dict(msg=e.detail), status_code=e.status_code)


@router.delete("/{comment_id}", dependencies=[Depends(oauth2_scheme)])
async def delete_comment(
    comment_id: str = Path(..., title="The comment id to delete"),
    session: Session = Depends(get_session),
    authorization: Optional[str] = Header(None),
):
    try:
        comment = comments.check_comment_exist(session, comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="COMMENT_DOES_NOT_EXIST")
        payload = users.decode_token(authorization)
        if payload.type_id != 1 and comment.user_id != payload.user_id:
            raise HTTPException(status_code=403, detail="UNAUTHORIZED")
        comments.delete_comment(session, comment_id)
    except HTTPException as e:
        return JSONResponse(content=dict(msg=e.detail), status_code=e.status_code)


@router.patch("/{comment_id}", dependencies=[Depends(oauth2_scheme)])
async def update_comment(
    comment: CommentBase,
    comment_id: str = Path(..., title="The comment id to update"),
    session: Session = Depends(get_session),
    authorization: Optional[str] = Header(None),
):
    try:
        comment = comments.check_comment_exist(session, comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail="COMMENT_DOES_NOT_EXIST")
        payload = users.decode_token(authorization)
        if payload.type_id != 1 and comment.user_id != payload.user_id:
            raise HTTPException(status_code=403, detail="UNAUTHORIZED")
        comments.update_comment(session, comment_id)
    except HTTPException as e:
        return JSONResponse(content=dict(msg=e.detail), status_code=e.status_code)
