from typing import Union
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import engine
from app.models import * # import all models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # start up
    Base.metadata.create_all(bind=engine) # init db
    yield
    # shut down

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}