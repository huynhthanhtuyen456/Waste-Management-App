from pydantic import BaseModel
from odmantic import Model, ObjectId

from app.utils.enums import ChallengeDifficultyEnum


class ChallengeRequestModel(BaseModel):
    name: str
    description: str | None = None
    difficulty_level: ChallengeDifficultyEnum
    scoring_criteria: list[ObjectId]


class ChallengeResponseModel(Model):
    name: str
    description: str | None = None
    difficulty_level: ChallengeDifficultyEnum
    scoring_criteria: list[ObjectId]


class ChallengeDeleteResponseModel(BaseModel):
    message: str