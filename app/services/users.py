from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from starlette import status

from app.config import get_settings
from app.db.session import engine
from app.models.users import User, AccessToken


async def get_user(email: str):
    user = await engine.find_one(User, User.email == email)
    if user:
        return user


async def get_current_user(token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"Authorization": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token.credentials,
            get_settings().secret_key,
            algorithms=[get_settings().algorithm],
        )
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(email=email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user