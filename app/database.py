from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pydantic import BaseSettings


BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: str

    class Config:
        env_file = str(BASE_DIR / ".env")


db_setting = Settings()

DATABASE_URL = (
    "mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}?charset=utf8mb4".format(
        USER=db_setting.DB_USER,
        PASSWORD=db_setting.DB_PASSWORD,
        HOST=db_setting.DB_HOST,
        NAME=db_setting.DB_NAME,
        PORT=db_setting.DB_PORT,
    )
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
