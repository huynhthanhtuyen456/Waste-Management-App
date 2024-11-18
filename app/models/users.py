from datetime import datetime

from odmantic import Model, Reference, Field
from pydantic import EmailStr

from app.models.roles import Role
from app.utils.enums import ScoreRankEnum


def datetime_now_sec():
    return datetime.now().replace(microsecond=0)


class AccessToken(Model):
    email: EmailStr
    token: str


class ScoreRank(Model):
    score: int
    level: ScoreRankEnum



class User(Model):
    email: EmailStr = Field(unique=True, index=True)
    hashed_password: str
    first_name: str = Field(default="", index=True)
    last_name: str = Field(default="", index=True)
    is_active: bool = Field(default=True)
    role: Role = Reference()
    score: int = Field(default=0)
    rank: ScoreRank | None = Field(default=None)
