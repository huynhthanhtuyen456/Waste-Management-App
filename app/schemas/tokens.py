from pydantic import BaseModel


class TokenResponseModel(BaseModel):
    access_token: str
    token_type: str