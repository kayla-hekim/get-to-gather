# app/main.py
from fastapi import FastAPI
from app.models import User, Calendar, Event

app = FastAPI()

@app.get("/")
def read_root():
    return {}
