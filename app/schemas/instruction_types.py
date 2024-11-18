from odmantic import Model
from pydantic import BaseModel


class WasteInstructionTypeRequestModel(BaseModel):
    type: str
    description: str | None = None


class WasteInstructionTypeResponseModel(Model):
    type: str
    description: str | None = None


class WasteInstructionTypeDeleteResponseModel(BaseModel):
    message: str
