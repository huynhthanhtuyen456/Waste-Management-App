from pydantic import BaseModel, EmailStr

from app.models.roles import Role
from app.utils.enums import RoleEnum


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class UserIn(BaseModel):
    email: EmailStr
    hashed_password: str
    first_name: str | None = None
    last_name: str | None = None


class UserOut(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None


class UserCreate(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    password: str
    is_active: bool = True
    is_superuser: bool = False
    role: Role | None = None

    def assign_role(self, role: RoleEnum):
        if role:
            role = Role.find_one({"name": role.member})
            self.role = Role(name=role["name"], description=role["description"], id=role["_id"])
