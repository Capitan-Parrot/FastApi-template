import pytest
from redis import Redis
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.auth import authenticate_user
from app.services.users import create_user, get_user_by_email, get_user_by_id
from app.tests.utils import create_user_schema
from app.schemas.users import UserBase


async def test_create_user(db: Session, redis: Redis):
    user_in = create_user_schema()

    user = await create_user(db, redis, user_in)

    assert user.email == user_in.email
    assert hasattr(user, "hashed_password")


async def test_create_user_that_exists(db: Session, redis: Redis):
    user_in, email = create_user_schema()

    with pytest.raises(HTTPException):
        await create_user(db, redis, user_in)


async def test_get_user_by_email(db: Session, redis: Redis):
    user_in = create_user_schema()
    registered_user = await create_user(db, user_in)

    user = get_user_by_email(db, registered_user.email)

    assert user == registered_user


async def test_get_user_by_id(db: Session, redis: Redis):
    user_in = create_user_schema()
    registered_user, password = create_user(db, user_in)

    user = await get_user_by_id(db, redis, registered_user.id)

    assert user == registered_user


async def test_authenticate_user(db: Session, redis: Redis):
    user_in = create_user_schema()
    registered_user = await create_user(db, redis, user_in)
    login_in = UserBase(email=registered_user.email, password=user_in.password)

    login_user = await authenticate_user(db, login_in)

    assert registered_user == login_user


def test_authenticate_user_fail(db: Session):
    user_in = create_user_schema()

    with pytest.raises(HTTPException):
        authenticate_user(db, user_in)