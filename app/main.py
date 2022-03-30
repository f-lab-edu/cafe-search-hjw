import uvicorn
from fastapi import FastAPI

from routers import users
from schemas.common import ServerSettings


app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])


if __name__ == "__main__":
    server = ServerSettings()
    uvicorn.run(
        "main:app",
        host=server.SERVER_HOST,
        port=server.SERVER_PORT,
        reload=server.RELOAD,
    )
