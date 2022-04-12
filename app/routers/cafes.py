from fastapi import APIRouter, HTTPException, Depends, Path, Security
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session


from database import get_session
from schemas.cafes import CafeBase, CafeUpdate
from services import cafes
from .users import get_acitve_user

router = APIRouter()


@router.post("", dependencies=[Security(get_acitve_user, scopes=["admin"])])
async def apply_cafe(
    cafe: CafeBase,
    session: Session = Depends(get_session),
):
    if cafes.check_cafe_exist_by_name(session, cafe.name):
        raise HTTPException(status_code=409, detail="CAFE_ALREADY_EXIST")
    cafes.create_cafe(session, cafe)
    return JSONResponse(content=dict(msg="CREATE_SUCCESS"), status_code=201)


@router.delete("/{cafe_id}", dependencies=[Security(get_acitve_user, scopes=["admin"])])
async def delete_cafe(
    cafe_id: int = Path(..., title="The cafe id to delete"),
    session: Session = Depends(get_session),
):
    cafe = cafes.check_cafe_exist_by_id(session, cafe_id)
    if not cafe:
        raise HTTPException(status_code=404, detail="CAFE_DOES_NOT_EXIST")
    cafes.delete_cafe(session, cafe_id)
    return JSONResponse(content=dict(msg="DELETE_SUCCESS"), status_code=201)


@router.patch("/{cafe_id}", dependencies=[Security(get_acitve_user, scopes=["admin"])])
async def update_cafe(
    cafe: CafeUpdate,
    cafe_id: int = Path(..., title="The cafe id to update"),
    session: Session = Depends(get_session),
):
    if not cafe.dict(exclude_none=True):
        raise HTTPException(status_code=400, detail="INVALIED_FIELD")
    if not cafes.check_cafe_exist_by_id(session, cafe_id):
        raise HTTPException(status_code=404, detail="CAFE_DOES_NOT_EXIST")
    cafes.update_cafe(session, cafe_id, cafe)
    return JSONResponse(content=dict(msg="UPDATE_SUCCESS"), status_code=200)
