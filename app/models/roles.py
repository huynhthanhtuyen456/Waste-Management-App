from bson import ObjectId
from odmantic import Model, Reference


class Permission(Model):
    name: str
    description: str | None = None


class Role(Model):
    name: str
    description: str | None = None
    permission_ids: list[ObjectId]
