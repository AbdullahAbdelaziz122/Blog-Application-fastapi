from fastapi import APIRouter, Depends, status
from typing import  List
from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from ..repository import userRepository


router = APIRouter(
    prefix="/user",
    tags=['User']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(request: schemas.User, db: Session = Depends (get_db)):
    return userRepository.create_user(request, db)

@router.get("/", response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return userRepository.get_all_users(db)


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    return userRepository.get_user(id, db)



@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED, response_model = schemas.UserResponse)
def update_user(request: schemas.User ,id: int, db: Session = Depends(get_db)):
    return userRepository.update_user(request, id, db)


@router.delete("/{id}" ,tags=["User"])
def delete_user(id: int, db: Session = Depends (get_db)):
    return userRepository.delete_user(id, db)

