from jose import jwt, JWTError
from starlette import status
from typing import Annotated

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.core.security import verify_password, oauth2_scheme
from app.models import User
from app.schemas.tokens import TokenData
from app.schemas.users import UserLogin
from app.services.users import get_user_by_email
from app.database import get_db


def authenticate_user(db: Session, user: UserLogin) -> User:
    db_user = get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Пользователь с такой почтой не существует")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверная пара почта/пароль")
    return db_user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    db = get_db()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.hash_algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
