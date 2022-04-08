from sqlalchemy.orm import Session

from schemas.common import Cafe
from schemas.cafes import CafeBase, CafeUpdate
from models import models


def create_cafe(session: Session, cafe: CafeBase):
    new_cafe = models.Cafe(
        name=cafe.name,
        address=cafe.address,
        lat=cafe.lat,
        lon=cafe.lon,
        rep_number=cafe.rep_number,
    )
    session.add(new_cafe)
    session.commit()


def check_cafe_exist_by_name(session: Session, cafe_name: str) -> Cafe:
    cafe = session.query(models.Cafe).filter(models.Cafe.name == cafe_name).first()
    if cafe:
        return cafe


def check_cafe_exist_by_id(session: Session, cafe_id: int) -> Cafe:
    cafe = session.query(models.Cafe).filter(models.Cafe.id == cafe_id).first()
    if cafe:
        return cafe


def delete_cafe(session: Session, cafe_id: int):
    session.query(models.Cafe).filter(models.Cafe.id == cafe_id).delete()
    session.commit()


def update_cafe(session: Session, cafe_id: int, cafe: CafeUpdate):
    session.query(models.Cafe).filter(models.Cafe.id == cafe_id).update(
        cafe.dict(exclude_none=True)
    )
    session.commit()
