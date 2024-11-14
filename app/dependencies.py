from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.utils.utils import get_current_user


async def get_token_header(token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]):
    user = await get_current_user(token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token.")
