from fastapi import APIRouter, Depends,Response, status
from typing import List
from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from ..repository import blogRepository




router = APIRouter(
    prefix= "/blog",
    tags=['Blog']
)

@router.post("/", status_code=201, response_model=schemas.BlogResponse)
def create(request: schemas.BlogBase, db: Session = Depends(get_db)):
   
    return blogRepository.create(request, db)

@router.get('/', response_model=List[schemas.ShowBlog])
def get_all(db: Session = Depends(get_db)):
    
    return blogRepository.get_all_blogs(db)



@router.get('/{id}', response_model=schemas.ShowBlog)
def show(id, response: Response, db: Session = Depends(get_db)):
   return blogRepository.get_blog(id, response, db)




@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowBlog)
def update(id: int, request: schemas.BlogBase, db: Session = Depends(get_db)):
   return blogRepository.update(id, request, db)





@router.delete("/{id}")
def delete(id, db: Session = Depends(get_db)):
   return blogRepository.delete(id, db)