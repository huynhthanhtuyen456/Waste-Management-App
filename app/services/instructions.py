from odmantic import ObjectId
from pydantic import ValidationError

from app.db import engine
from app.models.instructions import WasteInstruction, WasteInstructionType
from app.schemas.instructions import InstructionRequestModel
from app.schemas.instruction_types import WasteInstructionTypeRequestModel

class WasteInstructionTypeService:
    engine = engine
    model = WasteInstructionType

    async def get_type_by_id(self, type_id: ObjectId):
        instruction_type = await self.engine.find_one(self.model, self.model.id == type_id)
        if instruction_type:
            return instruction_type

    async def find_one_by_type(self, _type: str):
        instruction_type = await self.engine.find_one(self.model, self.model.type == _type)
        if instruction_type:
            return instruction_type

    async def find_types(self, filters: dict):
        instructions = await self.engine.find(self.model, filters)
        return instructions

    async def create_instruction_type(self, instance: WasteInstructionType):
        try:
            inserted_data = await self.engine.save(instance)
        except TypeError as e:
            raise ValidationError(e)
        else:
            return inserted_data

    async def update_instruction_type(
            self,
            instance: WasteInstructionType,
            update_instance: WasteInstructionTypeRequestModel
    ):
        instance.model_update(update_instance)
        updated_instance = await engine.save(instance)
        return updated_instance

    async def delete_instruction_type(self, instance: WasteInstructionType):
        await engine.delete(instance)


class WasteInstructionService:
    engine = engine
    model = WasteInstruction

    async def get_instruction_by_id(self, instruction_id: ObjectId):
        instruction = await self.engine.find_one(self.model, self.model.id == instruction_id)
        if instruction:
            return instruction

    async def create_instruction(self, instance: WasteInstruction):
        try:
            inserted_data = await self.engine.save(instance)
        except TypeError as e:
            raise ValidationError(e)
        else:
            return inserted_data

    async def update_instruction(self, instance: WasteInstruction, update_instance: InstructionRequestModel):
        instance.model_update(update_instance)
        updated_instance = await engine.save(instance)
        return updated_instance

    async def delete_instruction(self, instance: WasteInstruction):
        await engine.delete(instance)

    async def find_instructions(self, filters: dict):
        instructions = await self.engine.find(self.model, filters)
        return instructions


instruction_type_service = WasteInstructionTypeService()
instruction_service = WasteInstructionService()
__all__ = ["instruction_type_service", "instruction_service"]
