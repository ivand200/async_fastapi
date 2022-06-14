from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    post_id: int
    content: str
    publication_date: datetime = Field(default_factory=datetime.now)

    class Config:
        orm_mode = True


class CommentCreate(CommentBase):
    pass

    class Config:
        orm_mode = True


class CommentPublic(CommentBase):
    id: int

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    pass

    class Config:
        orm_mode = True


class PostPublic(PostBase):
    id: int
    comments: Optional[List[CommentPublic]]

    class Config:
        orm_mode = True


class PostPartialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

    class Config:
        orm_mode = True
