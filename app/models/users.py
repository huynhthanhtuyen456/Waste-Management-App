from pydantic import EmailStr

from app.models.roles import Role
from app.utils.models import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    role: Role | None = None


class User(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    role: Role
