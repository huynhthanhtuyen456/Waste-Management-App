import datetime
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError

from app.db.session import engine
from app.models.users import AccessToken
from starlette import status

from app.config import get_settings


async def verify_jwt_token(token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token.credentials,
            get_settings().secret_key,
            algorithms=[get_settings().algorithm]
        )
        email: str = payload.get("email")
        exp: int = payload.get("exp")
        if datetime.datetime.fromtimestamp(exp) < datetime.datetime.utcnow():
            credentials_exception.detail = "Token expired!"
            raise credentials_exception
        if email is None:
            raise credentials_exception
        token = await engine.find_one(AccessToken, {"email": email, "token": token.credentials})
        if not token:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
