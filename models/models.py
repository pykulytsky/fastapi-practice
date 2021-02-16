from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from passlib.hash import pbkdf2_sha256
import jwt
from datetime import datetime
from datetime import timedelta

from app import settings

from .database import Base
from .exceptions import JwtTokenError


class User(Base):
    username = Column(String, primary_key=True, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)

    password = Column(String)
    email = Column(String)

    is_superuser = Column(Boolean, default=False)

    articles = relationship("Item", back_populates="author")

    def __init__(
        self,
        username: str,
        first_name: str,
        last_name: str,
        password: str,
        email: str
    ) -> None:
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

        self.set_password(password)

    def set_password(self, password: str) -> str:
        self.password = pbkdf2_sha256.hash(
            password,
            salt=bytes(settings.SECRET_KEY.encode('utf-8'))
        )
        return self.password

    @property
    def token(self):
        return self.generate_jwt_token()

    def generate_jwt_token(self):
        period = datetime.now() + timedelta(days=60)
        try:
            token = jwt.encode({
                'username': self.username,
                'exp': period.timestamp(),
                'is_superuser': int(self.is_superuser)
            }, settings.SECRET_KEY, algorithm='HS256')

        except Exception:
            raise JwtTokenError("Error occured, while generating JWT token.")

        return token.decode('utf-8')


class Article(Base):
    title = Column(String)
    description = Column(String)
    views = Column(Integer, default=0)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship('User', back_populates="article")
