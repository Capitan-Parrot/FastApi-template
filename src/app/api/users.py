from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.schemas.users import UserBase, UserRegister, UserLogin

from app.database import get_db
from app.services.users import create_user, get_user_by_id, get_user_by_email, authenticate_user, delete, get_users

router = APIRouter(prefix="/users", tags=["user"])


@router.get("/", response_model=list[UserBase])
def index(db: Session = Depends(get_db)):
    all_users = get_users(db)
    return all_users


@router.get("/{user_id}", response_model=UserBase)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=400, detail="Пользователя не существует")
    return user


@router.post("/register", response_model=UserBase)
def register(register_request: UserRegister, db: Session = Depends(get_db)):
    user = get_user_by_email(db, register_request.email)
    if user:
        raise HTTPException(status_code=400, detail="Пользователь с такой почтой уже существует")
    # request = UserService.get_register_request_by_email(db, register_request.email)
    # if request:
    #     raise HTTPException(status_code=400, detail="Ваш запрос уже существует")
    user, hash_password = create_user(db, register_request)
    return user


@router.post("/login", response_model=UserBase)
def login(login_request: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_request)
    if not user:
        raise HTTPException(status_code=400, detail="Почта или пароль некорректны")
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
