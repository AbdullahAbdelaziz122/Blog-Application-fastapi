from typing import List
from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    name : str
    email : str
    password : str


class BlogBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = None
    user_id: int
    


class ShowBlog(BaseModel):
    title: str
    content: str
    published: Optional[bool] = None
    
class UserResponse(BaseModel):
    name: str
    email: str
    blogs: List[ShowBlog]

    class Config:
        from_attributes = True

    


class BlogResponse(BaseModel):
    title: str
    content: str
    published: Optional[bool]
    creator: UserResponse

    class Config:
        from_attributes = True


class Login(BaseModel):
    username: str
    password: str