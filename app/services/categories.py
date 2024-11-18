from app.db import engine
from app.models.categories import WasteCategory
from app.services.base_service import BaseService


class CategoryService(BaseService):
    pass


category_service = CategoryService(db_model=WasteCategory, db_engine=engine)
__all__ = ["category_service"]
