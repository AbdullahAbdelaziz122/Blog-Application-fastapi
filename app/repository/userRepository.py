from fastapi import APIRouter, Depends,Response, status
from fastapi import HTTPException
from typing import  List
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from ..hashing import Hash


hash = Hash()


def create_user(request: schemas.User, db: Session = Depends (get_db)):
    new_user = models.User(name = request.name, email = request.email, password = hash.get_password_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users



def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        print("User not found man")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    return user


def update_user(request: schemas.User ,id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {request.id} not found")
    
    user.name = request.name
    user.email = request.email
    if request.password:
        user.password = hash.get_password_hash(request.password)
    db.commit()
    db.refresh(user)
    return user


def delete_user(id: int, db: Session = Depends (get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    
    db.delete(user)
    db.commit()
    return "User Has been deleted"