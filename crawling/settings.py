import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(str(BASE_DIR / ".env"))

API_KEY = os.environ.get("API_KEY")
DATABASE_URL = (
    "mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}?charset=utf8mb4".format(
        USER=os.environ.get("DB_USER"),
        PASSWORD=os.environ.get("DB_PASSWORD"),
        HOST=os.environ.get("DB_HOST"),
        NAME=os.environ.get("DB_NAME"),
        PORT=os.environ.get("DB_PORT"),
    )
)
engine = create_engine(DATABASE_URL)

GU_LIST = [
    "강남구",
    "강동구",
    "강북구",
    "강서구",
    "관악구",
    "광진구",
    "구로구",
    "금천구",
    "노원구",
    "도봉구",
    "동대문구",
    "동작구",
    "마포구",
    "서대문구",
    "서초구",
    "성동구",
    "성북구",
    "송파구",
    "양천구",
    "영등포구",
    "용산구",
    "은평구",
    "종로구",
    "중구",
    "중랑구",
]
