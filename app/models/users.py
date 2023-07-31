from sqlalchemy import Column, Integer, String, Boolean

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    role = Column(String, default='USER')
    hashed_password = Column(String)
    is_banned = Column(Boolean, default=False)