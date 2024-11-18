from pydantic import BaseModel
from odmantic import Model, ObjectId, Reference

from app.models.wastes import WasteCategory
from app.models.instructions import WasteInstructionType


class InstructionRequestModel(BaseModel):
    title: str
    content: str
    type_id: ObjectId
    category_id: ObjectId


class InstructionResponseModel(Model):
    title: str
    content: str
    type: WasteInstructionType = Reference()
    category: WasteCategory = Reference()


class InstructionDeleteResponseModel(BaseModel):
    message: str
