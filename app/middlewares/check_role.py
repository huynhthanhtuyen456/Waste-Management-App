from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status

from app.models.users import User
from app.services.users import get_current_active_user


class RoleChecker:
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def __call__(self, user: Annotated[User, Depends(get_current_active_user)]):
        if user.role.name.lower() in self.allowed_roles or user.is_superuser:
            return True
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You don't have enough permissions"
        )