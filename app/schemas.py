from pydantic import BaseModel
from typing import Optional

class BlogBase(BaseModel):
    title: str
    content: str
    published: Optional[bool]



class BlogResponse(BlogBase):
    title: str
    content: str
    published: Optional[bool]

    class Config:
        orm_mode = True
