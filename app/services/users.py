from fastapi import HTTPException, Depends
from passlib.context import CryptContext

from app.repositories.user.postgresql import UserRepository, get_user_repository
from app.repositories.user.redis import UserRepositoryCache, get_user_repository_cache
from app.schemas.users import UserBase, User
from app.core.security import get_password_hash

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, db: UserRepository, cache: UserRepositoryCache) -> None:
        self.db = db
        self.cache = cache

    async def delete(self, user_id: int) -> None:
        await self.cache.delete(user_id)
        self.db.delete(user_id)

    async def update(self, user_id: int, user_data: UserBase) -> User:
        user = await self.cache.get(user_id)
        if not user:
            user = self.db.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=400, detail="Пользователь не существует")

        for key, value in user_data:
            if key == "password":
                setattr(user, "hashed_password", get_password_hash(value))
            else:
                setattr(user, key, value)
        await self.cache.set(user_id, user)
        self.db.update(user)

        return user

    async def create_user(self, user: UserBase) -> User:
        curr_user = self.db.get_user_by_email(user.email)
        if curr_user:
            raise HTTPException(status_code=400, detail="Пользователь с такой почтой уже существует")

        curr_user = self.db.create(user)
        await self.cache.set(curr_user.id, curr_user)

        return curr_user

    def get_users(self) -> list[User]:
        users = self.db.get_users()
        return users

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.cache.get(user_id)
        if not user:
            user = self.db.get_user_by_id(user_id)
        return user

    async def get_user_by_email(self, email: str) -> User:
        user = self.db.get_user_by_email(email)
        await self.cache.set(user.id, user)
        return user


def get_user_service(user_repository: UserRepository = Depends(get_user_repository),
                     user_repository_cache: UserRepositoryCache =
                     Depends(get_user_repository_cache)) -> UserService:
    user_service = UserService(user_repository, user_repository_cache)
    return user_service
