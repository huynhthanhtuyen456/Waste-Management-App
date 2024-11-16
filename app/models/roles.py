from app.db import RoleCollection
from app.models.permissions import Permission
from app.utils.models import BaseModel


class Role(BaseModel):
    name: str
    description: str | None = None

    def save(self):
        return RoleCollection.insert_one(self.__dict__)

    @staticmethod
    def find_one(filters: dict) -> dict:
        return RoleCollection.find_one(filters)


class RolePermission(BaseModel):
    role: Role
    permission: Permission