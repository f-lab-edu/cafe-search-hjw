import uvicorn
from fastapi import FastAPI

from routers import users
from config import settings
from models.models import Base
from database import engine


Base.metadata.create_all(engine)
app = FastAPI()
app.include_router(users.router, prefix="/users", tags=["users"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.RELOAD,
    )
