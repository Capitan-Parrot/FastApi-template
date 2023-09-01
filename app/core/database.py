from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings import settings


def get_url():
    user = settings.postgres_user
    password = settings.postgres_password
    server = settings.postgres_server
    db = settings.postgres_db
    return f"postgresql://{user}:{password}@{server}/{db}"


engine = create_engine(get_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
