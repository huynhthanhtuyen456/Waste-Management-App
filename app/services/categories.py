from odmantic import ObjectId
from app.db import engine
from app.models.categories import WasteCategory


class CategoryService:
    engine = engine
    model = WasteCategory

    async def get_category_by_id(self, category_id: ObjectId):
        category = await self.engine.find_one(self.model, self.model.id == category_id)
        if category:
            return category


category_service = CategoryService()
__all__ = ["category_service"]
