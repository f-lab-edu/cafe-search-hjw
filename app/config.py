from pathlib import Path

from pydantic import BaseSettings


BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 8000
    RELOAD: bool = True

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: str

    TOKEN_SECRET_KEY: str
    HASHING_ALGORITHM: str

    class Config:
        env_file = str(BASE_DIR / ".env")


settings = Settings()
