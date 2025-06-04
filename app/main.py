# app/main.py
from fastapi import FastAPI
from app.routes import auth
from app.models import User, Calendar, Event
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {}
