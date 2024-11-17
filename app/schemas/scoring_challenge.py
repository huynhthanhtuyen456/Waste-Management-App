from pydantic import BaseModel
from odmantic import Model, ObjectId


class ScoringCriteriaRequestModel(BaseModel):
    criteria: str
    score: int


class ScoringCriteriaResponseModel(Model):
    criteria: str
    score: int


class ScoringCriteriaDeleteResponseModel(BaseModel):
    message: str