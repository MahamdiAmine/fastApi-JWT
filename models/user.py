from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DATETIME, String, Integer, JSON

from database import Base, engine
from sqlalchemy_utils import EmailType


class AuthModel(BaseModel):
    email: str
    username: str
    password: str


class UserDB(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(EmailType)
    username = Column(String(50))
    password = Column(String(100))
    created_at = Column(DATETIME())
    updated_at = Column(DATETIME())
    is_active = Column(Boolean)
    roles = Column(JSON)


Base.metadata.create_all(bind=engine)
