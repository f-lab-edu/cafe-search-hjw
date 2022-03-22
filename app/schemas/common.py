from pydantic import BaseSettings


class ServerSettings(BaseSettings):
    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 8000
    RELOAD: bool = True
