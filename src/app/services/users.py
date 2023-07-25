from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import secrets
import string
from app.schemas.users import UserRegister, UserBase, UserLogin
from app.models.users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_users(db, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user_by_email(db, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


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


def create_user(db: Session, user: UserRegister) -> (User, str):
    curr_user = get_user_by_email(db, user.email)
    if curr_user:
        raise HTTPException(status_code=400, detail="Пользователь с такой почтой уже существует")
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(20))  # for a 20-character password
    hashed_password = get_password_hash(password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user, password


def authenticate_user(db: Session, user: UserLogin) -> User:
    db_user = get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Пользователь с такой почтой не существует")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверная пара почта/пароль")
    return db_user
