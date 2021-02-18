from typing import Union
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_or_false(db: Session, user_id: int) -> Union[models.User, bool]:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        return user
    else:
        return False


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    user = models.User(
        email=user.email,
        username=user.username,
        password=user.password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_articles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Article).offset(skip).limit(limit).all()


def get_article(db: Session, id: int):
    return db.query(
        models.User
    ).filter(models.Article.id == id).first()


def create_user_article(
    db: Session,
    article: schemas.ArticleCreate,
    user_id: int
):
    db_article = models.Article(**article.dict(), author_id=user_id)
    db_article = models.Article(**article.dict(), author_id=user_id)
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article
