from aioredis import ConnectionPool
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.core.database import SessionLocal
from app.__main__ import app


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="session")
def redis() -> Generator:
    yield ConnectionPool()


@pytest.fixture(scope="session")
def redis() -> Generator:
    yield ConnectionPool()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c

