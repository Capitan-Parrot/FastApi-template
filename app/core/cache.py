import redis

from app.settings import settings


def create_redis():
    return redis.ConnectionPool(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password,
        db=0,
        decode_responses=True
    )


pool = create_redis()


# Dependency
def get_redis():
    return redis.Redis(connection_pool=pool)
