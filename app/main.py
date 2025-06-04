# app/main.py
from fastapi import FastAPI
from app.routes import auth
from app.models import User, Calendar, Event

app = FastAPI()

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {}
