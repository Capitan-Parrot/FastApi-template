from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import secrets
import string
from app.schemas.users import UserRegister, UserBase
from app.models.users import User
from app.core.security import get_password_hash

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_users(db, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_email(db, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def delete(db, user_id: int):
    db.User.delete(user_id)


def update(db, user_id: int, user_data: UserBase):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=400, detail="Пользователь не существует")
    for key, value in user_data:
        if key == "password":
            setattr(user, "hashed_password", get_password_hash(value))
        else:
            setattr(user, key, value)


def create_user(db: Session, user: UserRegister) -> User:
    curr_user = get_user_by_email(db, user.email)
    if curr_user:
        raise HTTPException(status_code=400, detail="Пользователь с такой почтой уже существует")
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



