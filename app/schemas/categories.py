from pydantic import BaseModel
from odmantic import Model


class CategoryRequestModel(BaseModel):
    name: str
    description: str | None = None


class CategoryResponseModel(Model):
    name: str
    description: str | None = None


class CategoryDeleteResponseModel(BaseModel):
    message: str