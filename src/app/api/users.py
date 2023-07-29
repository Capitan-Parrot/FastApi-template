from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.users import UserBase
from app.services.users import get_user_by_id, delete, get_users
from app.models import User
from app.services.login import get_current_user

router = APIRouter(prefix="/users", tags=["user"])


@router.get("/", response_model=list[UserBase])
def index(db: Session = Depends(get_db)):
    all_users = get_users(db)
    return all_users


@router.get("/me", response_model=UserBase)
def get_me(user: Annotated[User, Depends(get_current_user)]):
    return user


@router.get("/{user_id}", response_model=UserBase)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=400, detail="Пользователя не существует")
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    delete(db, user_id)
    db.commit()


@router.put("/{user_id}", response_model=UserBase)
def update_user(user_id: int, user_data: UserBase, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    for key, value in user_data:
        setattr(user, key, value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
