import pickle
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from starlette import status

from app.config import get_settings
from app.db import engine
from app.models.users import User
from app.services.cache import cache
from app.utils.exceptions import EntityDoesNotExist


async def get_user(email: str):
    user = await engine.find_one(User, User.email == email)
    if user:
        return user


async def get_current_user(
        token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
        redis_client: cache = Depends(cache),
):
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

    if (cached_profile := redis_client.get(f"profile_{email}")) is not None:
        return pickle.loads(cached_profile)

    try:
        user = await get_user(email=email)
        redis_client.set(f"profile_{user.email}", pickle.dumps(user))

        if user is None:
            raise credentials_exception

        return user

    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user