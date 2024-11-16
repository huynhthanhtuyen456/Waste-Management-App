# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
from typing import Annotated, Optional

from pydantic import BeforeValidator, BaseModel, Field

PyObjectId = Annotated[str, BeforeValidator(str)]


class MongoBaseModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
