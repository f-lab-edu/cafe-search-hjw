import uvicorn
from fastapi import FastAPI

from schemas.common import ServerSettings


app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "UP"}


if __name__ == "__main__":
    server = ServerSettings()
    uvicorn.run(
        "main:app",
        host=server.SERVER_HOST,
        port=server.SERVER_PORT,
        reload=server.RELOAD,
    )
