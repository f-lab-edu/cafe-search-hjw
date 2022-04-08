import uvicorn
from fastapi import FastAPI

from routers import users
from config import settings


app = FastAPI()
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(users.router, prefix="/comments", tags=["comments"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.RELOAD,
    )
