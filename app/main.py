from fastapi import FastAPI, Response, status, HTTPException, Depends




from . import models, schemas, utilities
from .database import engine, get_db
from .routers import user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}



     