import pickle

from fastapi import HTTPException
from odmantic import ObjectId
from starlette import status

from app.config import settings
from app.db import engine
from app.models.categories import WasteCategory
from app.routes.categories import router
from app.schemas.categories import CategoryRequestModel, CategoryResponseModel, CategoryDeleteResponseModel
from app.services.cache import cache


@router.get('', summary="Get list of categories", response_model=list[CategoryResponseModel])
async def list_category(page: int = 1, page_break: bool = False):
    offset = {"skip": page * settings.MULTI_MAX, "limit": settings.MULTI_MAX} if page_break else {}

    if (cached_categories := cache().get(f"categories")) is not None:
        return pickle.loads(cached_categories)

    categories = await engine.find(WasteCategory, **offset)
    cache().set(f"categories", pickle.dumps(categories), ex=3600)

    return categories


@router.post('', summary="Create a new category", response_model=CategoryResponseModel)
async def create_category(category: CategoryRequestModel):
    # querying database to check if category already exists
    existed_category = await engine.find_one(WasteCategory, {"name": category.name})

    if existed_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category name={category.name} already exist"
        )

    new_category = WasteCategory(
        name=category.name,
        description=category.description,
    )
    inserted_category = await engine.save(new_category)

    return inserted_category


@router.get('/{category_id}', summary="Get a new category", response_model=CategoryResponseModel)
async def create_category(
        category_id: ObjectId
):
    # querying database to check if category already exists
    existed_category = await engine.find_one(WasteCategory, {"_id": category_id})

    if not existed_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found category with this id={category_id}"
        )

    return existed_category

@router.put('/{category_id}', summary="Update a new category", response_model=CategoryResponseModel)
async def update_category(
        category: CategoryRequestModel,
        category_id: ObjectId
):
    # querying database to check if category already exists
    existed_category = await engine.find_one(WasteCategory, {"_id": category_id})

    if not existed_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found category with this id={category_id}"
        )

    existed_category.model_update(category)
    await engine.save(existed_category)

    return existed_category


@router.delete('/{category_id}', summary="Delete a new category", response_model=CategoryDeleteResponseModel)
async def delete_category(
        category_id: ObjectId
):
    # querying database to check if category already exists
    existed_category = await engine.find_one(WasteCategory, {"_id": category_id})

    if not existed_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found category with this id={category_id}"
        )

    await engine.delete(existed_category)

    return CategoryDeleteResponseModel(message=f"Category deleted with id={category_id}")
