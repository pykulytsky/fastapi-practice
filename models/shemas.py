from typing import List, Optional

from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: str
    description: Optional[str] = None


class ArticleCreate(ArticleBase):
    pass


class Article(ArticleBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Article] = []

    class Config:
        orm_mode = True
