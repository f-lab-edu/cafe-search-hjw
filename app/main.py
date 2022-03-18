import uvicorn
from fastapi import FastAPI

from app.database import engine
from app.models import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

if __name__ == '__main__':
    uvicorn.run('app.main:app', host='localhost', port=8000, reload=True)
