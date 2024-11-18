from app.db import engine
from app.models.wastes import Waste
from app.services.base_service import BaseService


class WasteService(BaseService):
    async def find_wastes(self, filters: dict):
        wastes = await self.engine.find(self.model, filters)
        return wastes


waste_service = WasteService(db_model=Waste, db_engine=engine)
__all__ = ["waste_service"]
