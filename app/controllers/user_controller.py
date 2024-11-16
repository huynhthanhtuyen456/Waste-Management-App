from typing import Annotated

from fastapi import Depends

from app.models.users import User
from app.routes.users import router
from app.services.users import get_current_active_user
from app.schemas.users import UserProfileResponse, UserProfileUpdateRequestModel


@router.get("/me/", response_model=UserProfileResponse)
async def me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.put("/me/", response_model=UserProfileResponse)
async def me(
    current_user: Annotated[User, Depends(get_current_active_user)],
    profile: UserProfileUpdateRequestModel
):
    current_user.model_update(profile)
    return current_user