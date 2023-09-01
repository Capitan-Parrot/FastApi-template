from aioredis import Redis
from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from app.core.redis import get_redis
from app.models import UserDB
from app.schemas.users import UserBase


class UserRepositoryCache:
    def __init__(self, cache: Redis) -> None:
        self.cache = cache

    async def get(self, user_id: int) -> UserDB:
        user = await self.cache.hgetall(f'user:{user_id}')
        user['is_banned'] = bool(user['is_banned'])
        return UserDB(**user)

    async def get_multi(self, user_id: int) -> list[UserDB]:
        pass

    async def set(self, user_id: int, user: UserDB) -> None:
        user.is_banned = str(user.is_banned)
        await self.cache.hset(f'user:{user_id}', mapping=jsonable_encoder(user))
        user.is_banned = bool(user.is_banned)

    async def delete(self, user_id: int) -> None:
        await self.cache.delete(f'user:{user_id}')


def get_user_repository_cache(cache: Redis = Depends(get_redis)) -> UserRepositoryCache:
    user_repository_cache = UserRepositoryCache(cache)
    return user_repository_cache
