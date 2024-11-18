from app.db import engine
from app.models.instructions import WasteInstruction, WasteInstructionType
from app.services.base_service import BaseService


class WasteInstructionTypeService(BaseService):
    async def find_one_by_type(self, _type: str):
        instruction_type = await self.engine.find_one(self.model, self.model.type == _type)
        if instruction_type:
            return instruction_type

    async def find_types(self, filters: dict):
        instructions = await self.engine.find(self.model, filters)
        return instructions


class WasteInstructionService(BaseService):
    async def find_instructions(self, filters: dict):
        instructions = await self.engine.find(self.model, filters)
        return instructions


instruction_type_service = WasteInstructionTypeService(db_model=WasteInstructionType, db_engine=engine)
instruction_service = WasteInstructionService(db_model=WasteInstruction, db_engine=engine)
__all__ = ["instruction_type_service", "instruction_service"]
