import uvicorn
from fastapi import FastAPI, Depends,Response, status
from fastapi import HTTPException
from typing import Optional, List
from .database import engine, get_db
from sqlalchemy.orm import Session
from .hashing import Hash
from .routers import blog, user, authentication
from . import models, schemas




app = FastAPI()

models.Base.metadata.create_all(bind =engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(blog.router)