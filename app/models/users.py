from datetime import datetime

from odmantic import Model, Reference, Field
from pydantic import EmailStr

from app.models.roles import Role
from app.models.wastes import Waste


def datetime_now_sec():
    return datetime.now().replace(microsecond=0)


class AccessToken(Model):
    email: EmailStr
    token: str


class User(Model):
    email: EmailStr = Field(unique=True, index=True)
    hashed_password: str
    first_name: str = Field(default="", index=True)
    last_name: str = Field(default="", index=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    role: Role = Reference()
    waste_items: list[Waste] | None = None
