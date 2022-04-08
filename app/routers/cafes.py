from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Path, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session


from database import get_session
from schemas.cafes import CafeBase, CafeUpdate
from services import users, cafes
from .users import oauth2_scheme

router = APIRouter()


@router.post("", dependencies=[Depends(oauth2_scheme)])
async def apply_cafe(
    cafe: CafeBase,
    session: Session = Depends(get_session),
    authorization: Optional[str] = Header(None),
):
    try:
        if cafes.check_cafe_exist_by_name(session, cafe.name):
            raise HTTPException(status_code=409, detail="CAFE_ALREADY_EXIST")
        payload = users.decode_token(authorization)
        if payload.type_id != 1:
            raise HTTPException(status_code=403, detail="UNAUTHORIZED")
        cafes.create_cafe(session, cafe)
        return JSONResponse(content=dict(msg="CREATE_SUCCESS"), status_code=201)

    except HTTPException as e:
        return JSONResponse(content=dict(msg=e.detail), status_code=e.status_code)


@router.delete("/{cafe_id}", dependencies=[Depends(oauth2_scheme)])
async def delete_cafe(
    cafe_id: int = Path(..., title="The cafe id to delete"),
    session: Session = Depends(get_session),
    authorization: Optional[str] = Header(None),
):
    try:
        cafe = cafes.check_cafe_exist_by_id(session, cafe_id)
        if not cafe:
            raise HTTPException(status_code=404, detail="CAFE_DOES_NOT_EXIST")
        payload = users.decode_token(authorization)
        if payload.type_id != 1:
            raise HTTPException(status_code=403, detail="UNAUTHORIZED")
        cafes.delete_cafe(session, cafe_id)
        return JSONResponse(content=dict(msg="DELETE_SUCCESS"), status_code=201)

    except HTTPException as e:
        return JSONResponse(content=dict(msg=e.detail), status_code=e.status_code)


@router.patch("/{cafe_id}", dependencies=[Depends(oauth2_scheme)])
async def update_cafe(
    cafe: CafeUpdate,
    cafe_id: int = Path(..., title="The cafe id to update"),
    session: Session = Depends(get_session),
    authorization: Optional[str] = Header(None),
):
    try:
        if not cafe.dict(exclude_none=True):
            raise HTTPException(status_code=400, detail="INVALIED_FIELD")
        if not cafes.check_cafe_exist_by_id(session, cafe_id):
            raise HTTPException(status_code=404, detail="CAFE_DOES_NOT_EXIST")
        payload = users.decode_token(authorization)
        if payload.type_id != 1:
            raise HTTPException(status_code=403, detail="UNAUTHORIZED")
        cafes.update_cafe(session, cafe_id, cafe)
        return JSONResponse(content=dict(msg="UPDATE_SUCCESS"), status_code=200)

    except HTTPException as e:
        return JSONResponse(content=dict(msg=e.detail), status_code=e.status_code)
    except ValueError as e:
        return JSONResponse(content=dict(msg=e.detail), status_code=e.status_code)
