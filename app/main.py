from fastapi import FastAPI
from .database import engine
from . import models

from . import models
from .database import engine, get_db
from .routers import user, auth, order, currencies

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(currencies.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(order.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}