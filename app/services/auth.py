from jose import jwt, JWTError
from starlette import status
from typing import Annotated
from fastapi import HTTPException, Depends

from app.services.users import UserService, get_user_service
from app.settings import settings
from app.core.security import verify_password, oauth2_scheme
from app.schemas.tokens import TokenData
from app.schemas.users import UserBase, User


class AuthService:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    async def authenticate_user(self, user: UserBase) -> User:
        db_user = await self.user_service.get_user_by_email(user.email)
        if not db_user:
            raise HTTPException(status_code=400, detail="Пользователь с такой почтой не существует")
        if not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=400, detail="Неверная пара почта/пароль")
        return db_user

    async def get_current_user(self, token: str) -> User:
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
        user = await self.user_service.get_user_by_email(token_data.email)
        if user is None:
            raise credentials_exception
        return user


def get_auth_service(user_service: UserService = Depends(get_user_service)) -> AuthService:
    auth_service = AuthService(user_service)
    return auth_service
