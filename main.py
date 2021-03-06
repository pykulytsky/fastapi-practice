from typing import List
from auth.backend import JWTAuthentication

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from models import crud, models, schemas
from models.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.Token)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud.create_user(db=db, user=user)
    return {"token": new_user.token}


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get(
    "/users/{user_id}",
    response_model=schemas.User,
    dependencies=[Depends(JWTAuthentication())]
)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Article)
def create_item_for_user(
    user_id: int, article: schemas.ArticleCreate, db: Session = Depends(get_db)
):
    return crud.create_user_article(db=db, article=article, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Article])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    articles = crud.get_articles(db, skip=skip, limit=limit)
    return articles
