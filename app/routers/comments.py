from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Path, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session


from database import get_session
from schemas.comments import CommentCreate, CommentBase
from services import users, comments
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
        user = users.check_user_exist(session, payload.username)
        if user:
            raise HTTPException(status_code=409, detail="USER_ALREADY_EXIST")
        comments.create_comment(comment, user.id, session)
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
        payload = users.decode_token(authorization)
        user = users.check_user_exist(session, username=payload.username)
        if not user:
            raise HTTPException(status_code=404, detail="USER_DOES_NOT_EXIST")
        if int(payload.type_id) != 1 and user.username != payload.username:
            raise HTTPException(status_code=403, detail="UNAUTHORIZED")
        
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
        pass
    except HTTPException as e:
        return JSONResponse(content=dict(msg=e.detail), status_code=e.status_code)
