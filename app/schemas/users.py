from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    role: str
    hashed_password: str
    is_banned: bool

    class ConfigDict:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr
    password: str


