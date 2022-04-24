import uvicorn
from fastapi import FastAPI

from routers import users, cafes, comments
from config import settings


app = FastAPI()
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
app.include_router(cafes.router, prefix="/cafes", tags=["cafes"])


@app.get("/health")
async def health_check():
    return {"status": "UP"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.RELOAD,
    )
