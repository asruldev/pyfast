from typing import List
from pydantic import BaseModel
from datetime import datetime

# Article inside UserDisplay
class Article(BaseModel):
  title: str
  content: str
  published: bool
  class Config():
    from_attributes = True

class UserBase(BaseModel):
  username: str
  email: str
  password: str

class UserDisplay(BaseModel):
  username: str
  email: str
  items: List[Article] = []
  class Config():
    from_attributes = True

# User inside ArticleDisplay
class User(BaseModel):
  id: int
  username: str
  class Config():
    from_attributes = True

class ArticleBase(BaseModel):
  title: str
  content: str
  published: bool
  creator_id: int

class ArticleDisplay(BaseModel):
  title: str
  content: str
  published: bool
  user: User
  class Config():
    from_attributes = True

class MessageBase(BaseModel):
    sender_id: int
    recipient_id: int
    content: str

class MessageCreate(MessageBase):
    """Schema untuk input pembuatan pesan baru"""
    pass

class MessageRead(MessageBase):
    """Schema untuk output pesan yang sudah disimpan"""
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True