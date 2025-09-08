from fastapi import APIRouter, Depends,Response, status
from fastapi import HTTPException
from typing import List
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session



def create(request: schemas.BlogBase, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, content = request.content, published = request.published, user_id = request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs



def get_blog(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Blog with id: {id} is not found")
        
    return blog





def update(id: int, request: schemas.BlogBase, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.title = request.title
    blog.content = request.content
    blog.published = request.published
    db.commit()
    db.refresh(blog)
    return blog






def delete(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Blog {id} is not found")

    db.delete(blog)
    db.commit()
    return f"Blog {id} Deleted Successfully"