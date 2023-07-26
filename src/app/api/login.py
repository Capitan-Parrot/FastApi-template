from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.users import UserBase, UserRegister, UserLogin
from app.services.users import create_user, get_user_by_email
from app.core.security import create_access_token
from app.core.settings import settings
from app.schemas.tokens import Token
from app.services.login import authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserBase)
def register(register_request: UserRegister, db: Session = Depends(get_db)):
    user = create_user(db, register_request)
    return user


@router.post("/login", response_model=UserBase)
def login(login_request: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_request)
    if not user:
        raise HTTPException(status_code=400, detail="Почта или пароль некорректны")
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db=Depends(get_db)
):
    user = authenticate_user(db, UserLogin(email=form_data.username, password=form_data.password))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
