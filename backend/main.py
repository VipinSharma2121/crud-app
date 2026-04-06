import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from fastapi import FastAPI
from routes.user import router
from database import init_db

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

app.include_router(router)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": "Backend API connected to DB - User Management Ready"}

