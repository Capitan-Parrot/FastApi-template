from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from app.core.security import oauth2_scheme
from app.schemas.users import UserBase, User
from app.services.auth import AuthService, get_auth_service
from app.services.users import get_user_service, UserService


router = APIRouter(prefix="/users", tags=["user"])


@router.get("/", response_model=list[User])
def index(user_service: UserService = Depends(get_user_service)):
    all_users = user_service.get_users()
    return all_users


@router.get("/me", response_model=User)
async def get_me(token: Annotated[str, Depends(oauth2_scheme)], auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.get_current_user(token)
    return user


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=400, detail="Пользователя не существует")
    return user


@router.delete("/{user_id}", response_model=bool)
async def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    await user_service.delete(user_id)
    return True


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_data: UserBase, user_service: UserService = Depends(get_user_service)):
    user = await user_service.update(user_id, user_data)
    return user
