from sqlalchemy.orm import Session

from schemas.common import Cafe
from models import models


def check_cafe_exist(session: Session, cafe_id: int) -> Cafe:
    comment = session.query(models.Cafe).filter(models.Cafe.id == cafe_id).first()
    if comment:
        return comment
