from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_password_hash
from app.models import UserDB
from app.schemas.users import UserBase


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def delete(self, user_id: int) -> None:
        self.db.query(UserDB).filter_by(id=user_id).delete()
        self.db.commit()
    
    def update(self, user: UserDB) -> None:
        self.db.merge(user)
        self.db.commit()

    def create(self, user: UserBase) -> UserDB:
        hashed_password = get_password_hash(user["password"])
        db_user = UserDB(email=user["email"], hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_users(self, skip: int = 0, limit: int = 100) -> list[UserDB]:
        users = self.db.query(UserDB).offset(skip).limit(limit).all()
        return users

    def get_user_by_email(self, email: str) -> UserDB:
        user = self.db.query(UserDB).filter_by(email=email).first()
        return user

    def get_user_by_id(self, user_id: int) -> UserDB:
        user = self.db.query(UserDB).filter_by(id=user_id).first()
        return user


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    user_repository = UserRepository(db)
    return user_repository
