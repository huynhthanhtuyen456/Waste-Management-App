from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from odmantic import ObjectId
from starlette import status

from app.config import get_settings
from app.db import engine
from app.models.wastes import Waste
from app.routes.wastes import router
from app.schemas.wastes import WasteRequestModel, WasteResponseModel, WasteUpdateRequestModel, WasteDeleteResponseModel
from app.services.categories import category_service
from app.services.users import get_current_user
from app.services.wastes import waste_service


@router.get('', summary="Get list of wastes", response_model=list[WasteResponseModel])
async def list_waste(page: int = 1, page_break: bool = False):
    offset = {"skip": page * get_settings().MULTI_MAX, "limit": get_settings().MULTI_MAX} if page_break else {}  # noqa
    wastes = await waste_service.find_wastes(offset)

    return wastes


@router.post('', summary="Create a new waste", response_model=WasteResponseModel)
async def create_waste(
        waste: WasteRequestModel,
        token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]
):
    existed_waste = await waste_service.find_one({"name": waste.name})

    if existed_waste:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Waste with name={waste.name} already exists.",
        )

    if not waste.category_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category is missing"
        )

    category = await category_service.find_one({"_id": waste.category_id})

    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category not found ids={waste.category_id}."
        )

    user = await get_current_user(token)

    new_waste = Waste(
        name=waste.name,
        description=waste.description,
        user=user,
        category=category,
    )
    inserted_waste = await waste_service.create(new_waste)

    return inserted_waste


@router.get('/{waste_id}', summary="Get a waste", response_model=WasteResponseModel)
async def get_a_waste(
        waste_id: ObjectId
):
    existed_waste = await waste_service.get_by_id(waste_id)

    if not existed_waste:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found waste with this id={waste_id}"
        )

    return existed_waste

@router.put('/{waste_id}', summary="Update a new waste", response_model=WasteResponseModel)
async def update_category(
        waste: WasteUpdateRequestModel,
        waste_id: ObjectId
):
    existed_waste = await waste_service.get_by_id(waste_id)

    category = await category_service.find_one({"_id": waste.category_id})

    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category not found ids={waste.category_id}."
        )

    if not existed_waste:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found waste with this id={waste_id}"
        )

    await category_service.update(existed_waste, waste)

    return existed_waste


@router.delete('/{waste_id}', summary="Delete a waste", response_model=WasteDeleteResponseModel)
async def delete_waste(
        waste_id: ObjectId
):
    existed_waste = await waste_service.get_by_id(waste_id)

    if not existed_waste:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found waste with this id={waste_id}"
        )

    await waste_service.delete(existed_waste)

    return WasteDeleteResponseModel(message=f"Waste deleted with id={waste_id}")
