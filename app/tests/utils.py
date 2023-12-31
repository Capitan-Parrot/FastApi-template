import random
import string

from app.schemas.users import UserBase


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def create_user_schema() -> UserBase:
    email = f"{random_lower_string()}@{random_lower_string()}.com"
    password = "".join(random_lower_string())
    user_in = UserBase(email=email, password=password)
    return user_in


