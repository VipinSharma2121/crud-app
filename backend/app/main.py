from fastapi import FastAPI,Form, UploadFile, File
from database import engine
import models
from .routes import user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
