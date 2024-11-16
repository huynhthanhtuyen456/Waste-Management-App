from app.utils.models import BaseModel


class Permission(BaseModel):
    name: str
    description: str | None = None