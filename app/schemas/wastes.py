from odmantic import Model, Reference, ObjectId
from pydantic import BaseModel

from app.models.categories import WasteCategory
from app.models.users import User


class WasteRequestModel(BaseModel):
    name: str
    description: str | None = None
    category_id: ObjectId


class WasteUpdateRequestModel(BaseModel):
    name: str
    description: str | None = None
    category_id: ObjectId


class WasteResponseModel(Model):
    name: str
    description: str | None = None
    category: WasteCategory = Reference()


class WasteDeleteResponseModel(BaseModel):
    message: str