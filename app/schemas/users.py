from odmantic import Reference
from pydantic import BaseModel, EmailStr

from app.models.roles import Role
from app.models.users import ScoreRank


class UserAuthRequestModel(BaseModel):
    email: EmailStr
    password: str


class UserRegisterResponseModel(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None


class UserRegisterRequestModel(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    password: str


class UserProfileResponse(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool = True
    score: int
    role: Role = Reference()
    rank: ScoreRank | None = None


class UserProfileUpdateRequestModel(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
