import uvicorn
from fastapi import FastAPI, Depends,Response, status
from fastapi import HTTPException
from typing import Optional, List
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session




app = FastAPI()


models.Base.metadata.create_all(bind =engine)



@app.post("/blog", status_code=201)
def create(request: schemas.BlogBase, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, content = request.content, published = request.published)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.get('/blog', response_model=List[schemas.BlogResponse] )
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs
# Debugging


@app.get('/blog/{id}', response_model=schemas.BlogResponse)
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Blog with id: {id} is not found")
        
    return blog




@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.BlogResponse)
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





@app.delete("/blog/{id}")
def delete(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Blog {id} is not found")

    db.delete(blog)
    db.commit()
    return f"Blog {id} Deleted Successfully"
    


# if __name__ = "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)