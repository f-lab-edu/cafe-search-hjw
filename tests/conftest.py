from typing import Any
from typing import Generator
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "app"))
from models.models import Base, UserType
from database import get_session
from routers import users, cafes
from config import settings


def start_application():
    app = FastAPI()
    app.include_router(users.router, prefix="/users", tags=["users"])
    app.include_router(cafes.router, prefix="/cafes", tags=["cafes"])
    return app


SQLALCHEMY_DATABASE_URL = (
    "mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}?charset=utf8mb4".format(
        USER=settings.DB_USER,
        PASSWORD=settings.DB_PASSWORD,
        HOST=settings.DB_HOST,
        NAME="test",
        PORT=settings.DB_PORT,
    )
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    def _get_test_session():
        try:
            yield db_session
        finally:
            pass

    engine.execute(UserType.__table__.insert(), [{"type": "admin"}, {"type": "user"}])

    app.dependency_overrides[get_session] = _get_test_session
    with TestClient(app) as client:
        yield client
