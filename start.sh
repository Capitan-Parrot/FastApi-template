alembic upgrade head
uvicorn app.__main__:app --host 0.0.0.0 --port 8000