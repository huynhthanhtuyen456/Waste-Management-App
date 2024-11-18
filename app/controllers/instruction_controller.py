from fastapi import HTTPException
from odmantic import ObjectId
from starlette import status

from app.routes.instructions import router
from app.schemas.instructions import InstructionRequestModel, InstructionResponseModel, InstructionDeleteResponseModel
from app.models.instructions import WasteInstruction
from app.db import engine
from app.config import get_settings
from app.services.categories import category_service
from app.services.instructions import instruction_type_service, instruction_service


@router.get('', summary="Get list of waste instructions", response_model=list[InstructionResponseModel])
async def list_instructions(page: int = 1, page_break: bool = False):
    filters = {"skip": page * get_settings().MULTI_MAX, "limit": get_settings().MULTI_MAX} if page_break else {}  # noqa
    instructions = await instruction_service.find_instructions(filters=filters)

    return instructions


@router.post('', summary="Create a new waste instruction", response_model=InstructionResponseModel)
async def create_instruction(instruction: InstructionRequestModel):
    existed_instruction = await engine.find_one(WasteInstruction, {"title": instruction.title})

    category = await category_service.get_category_by_id(instruction.category_id)
    instruction_type = await instruction_type_service.get_type_by_id(instruction.type_id)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category does not exist",
        )

    if not instruction_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Typ of instruction does not exist",
        )

    if existed_instruction:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Instruction already exist"
        )

    new_instance = WasteInstruction(
        title=instruction.title,
        content=instruction.content,
        category=category,
        type=instruction_type
    )
    inserted_instruction = await instruction_service.create_instruction(new_instance)

    return inserted_instruction


@router.get('/{instruction_id}', summary="Get a instruction of waste", response_model=InstructionResponseModel)
async def get_instruction(instruction_id: ObjectId):
    # querying database to check if scoring_criteria already exists
    existed_instruction = await instruction_service.get_instruction_by_id(instruction_id)

    if not existed_instruction:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found Instruction with this id={instruction_id}"
        )

    return existed_instruction

@router.put('/{instruction_id}', summary="Update the instruction", response_model=InstructionResponseModel)
async def update_scoring_criteria(
        instruction: InstructionRequestModel,
        instruction_id: ObjectId
):
    # querying database to check if category already exists
    existed_instruction = await instruction_service.get_instruction_by_id(instruction_id)

    if not existed_instruction:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found instruction with this id={instruction_id}"
        )

    category = await category_service.get_category_by_id(instruction.category_id)
    instruction_type = await instruction_type_service.get_type_by_id(instruction.type_id)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category does not exist",
        )

    if not instruction_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Typ of instruction does not exist",
        )

    existed_instruction = await instruction_service.update_instruction(existed_instruction, instruction)

    return existed_instruction


@router.delete(
    '/{instruction_id}',
    summary="Delete a waste instruction",
    response_model=InstructionDeleteResponseModel
)
async def delete_scoring_criteria(
        instruction_id: ObjectId
):
    # querying database to check if category already exists
    existed_instruction = await instruction_service.get_instruction_by_id(instruction_id)

    if not existed_instruction:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found Instruction with this id={instruction_id}"
        )

    await engine.delete(existed_instruction)

    return InstructionDeleteResponseModel(message=f"Instruction deleted with id={instruction_id}")
