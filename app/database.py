from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import settings


DATABASE_URL = (
    "mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}?charset=utf8mb4".format(
        USER=settings.DB_USER,
        PASSWORD=settings.DB_PASSWORD,
        HOST=settings.DB_HOST,
        NAME=settings.DB_NAME,
        PORT=settings.DB_PORT,
    )
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# @contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
