from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    id: int
    email: str
    role: str
    hashed_password: str
    is_banned: bool

    class ConfigDict:
        from_attributes = True


class UserRegister(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
