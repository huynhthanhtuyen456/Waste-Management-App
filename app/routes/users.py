from typing import Annotated

from fastapi import APIRouter, Depends

from app.models.users import User
from app.utils.utils import get_current_active_user
from app.dependencies import get_token_header

router = APIRouter(
    prefix="/users",
    dependencies=[Depends(get_token_header)],
)


@router.get("/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@router.get("/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.email}]