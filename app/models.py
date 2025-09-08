from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from .database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    
    blogs = relationship("Blog", back_populates="creator")

class Blog (Base):
    
    __tablename__ = 'blog'
    

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    creator = relationship("User", back_populates="blogs")



