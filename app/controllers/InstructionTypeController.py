import pickle

from fastapi import HTTPException
from odmantic import ObjectId
from starlette import status

from app.config import settings
from app.models.instructions import WasteInstructionType
from app.routes.instruction_types import router
from app.schemas.instruction_types import WasteInstructionTypeRequestModel, WasteInstructionTypeResponseModel, \
    WasteInstructionTypeDeleteResponseModel
from app.services.cache import cache
from app.services.instructions import instruction_type_service


@router.get('', summary="Get list of instruction types", response_model=list[WasteInstructionTypeResponseModel])
async def list_instruction_types(page: int = 1, page_break: bool = False):
    filters = {"skip": page * settings.MULTI_MAX, "limit": settings.MULTI_MAX} if page_break else {}

    if (cached_instruction_types := cache().get(f"instruction_types")) is not None:
        return pickle.loads(cached_instruction_types)

    instruction_types = await instruction_type_service.find_types(filters=filters)
    cache().set(f"instruction_types", pickle.dumps(instruction_types), ex=3600)

    return instruction_types


@router.post('', summary="Create a new instruction type", response_model=WasteInstructionTypeResponseModel)
async def create_instruction_type(instruction_type: WasteInstructionTypeRequestModel):
    existed_instruction_type = await instruction_type_service.find_one_by_type(instruction_type.type)

    if existed_instruction_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type already exist"
        )

    new_instance = WasteInstructionType(
        type=instruction_type.type,
        description=instruction_type.description,
    )
    inserted_instruction = await instruction_type_service.create(new_instance)
    cache().delete(f"categories")
    return inserted_instruction


@router.get('/{type_id}', summary="Get the instruction type", response_model=WasteInstructionTypeResponseModel)
async def get_instruction_type(type_id: ObjectId):
    existed_instruction_type = await instruction_type_service.get_by_id(type_id)

    if not existed_instruction_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found Instruction Type with this id={type_id}"
        )

    return existed_instruction_type

@router.put('/{type_id}', summary="Update the instruction type", response_model=WasteInstructionTypeResponseModel)
async def update_instruction_type(
        instruction_type: WasteInstructionTypeRequestModel,
        type_id: ObjectId
):
    existed_instruction_type = await instruction_type_service.get_by_id(type_id)

    if not existed_instruction_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found Instruction Type with this id={type_id}"
        )

    existed_instruction_type = await instruction_type_service.update(
        existed_instruction_type,
        instruction_type
    )

    return existed_instruction_type


@router.delete(
    '/{type_id}',
    summary="Delete a instruction type by id",
    response_model=WasteInstructionTypeDeleteResponseModel
)
async def delete_instruction_type(type_id: ObjectId):
    existed_instruction_type = await instruction_type_service.get_by_id(type_id)

    if not existed_instruction_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found Instruction Type with this id={type_id}"
        )

    await instruction_type_service.delete(existed_instruction_type)

    return WasteInstructionTypeDeleteResponseModel(message=f"Instruction Type deleted with id={type_id}")
