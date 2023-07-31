import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.users import create_user, get_user_by_email, get_user_by_id, authenticate_user
from app.tests.utils import create_user_schema
from app.schemas.users import UserLogin


def test_create_user(db: Session):
    user_in = create_user_schema()

    user = create_user(db, user_in)

    assert user.email == user_in.email
    assert hasattr(user, "hashed_password")


def test_create_user_that_exists(db: Session):
    user_in, email = create_user_schema()

    with pytest.raises(HTTPException):
        create_user(db, user_in)


def test_get_user_by_email(db: Session):
    user_in = create_user_schema()
    registered_user = create_user(db, user_in)

    user = get_user_by_email(db, registered_user.email)

    assert user == registered_user


def test_get_user_by_id(db: Session):
    user_in = create_user_schema()
    registered_user, password = create_user(db, user_in)

    user = get_user_by_id(db, registered_user.id)

    assert user == registered_user


def test_authenticate_user(db: Session):
    user_in = create_user_schema()
    registered_user = create_user(db, user_in)
    login_in = UserLogin(email=registered_user.email, password=user_in.password)

    login_user = authenticate_user(db, login_in)

    assert registered_user == login_user


def test_authenticate_user_fail(db: Session):
    user_in = create_user_schema()

    with pytest.raises(HTTPException):
        authenticate_user(db, user_in)