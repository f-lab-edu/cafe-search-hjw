from typing import Tuple

from sqlalchemy.orm import Session

from schemas.common import Like


def get_or_create(session: Session, model, **kwargs) -> Tuple[Like, bool]:
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, True
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance, False
