from typing import TypeVar, Type

from odmantic import AIOEngine, ObjectId
from pydantic import BaseModel, ValidationError

from app.db import engine
from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService:
    def __init__(self, db_model: Type[ModelType], db_engine: AIOEngine):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A Mongo model class
        * `engine`: A MongoDb engine class
        """
        self.model = db_model
        self.engine = db_engine

    async def get_by_id(self, object_id: ObjectId):
        instance = await self.engine.find_one(self.model, self.model.id == object_id)
        if instance:
            return instance

    async def create(self, instance: CreateSchemaType):
        try:
            inserted_data = await self.engine.save(instance)
            return inserted_data
        except (ValidationError, TypeError) as e:
            raise ValidationError(e)

    async def update(
            self,
            instance: ModelType,
            update_instance: UpdateSchemaType
    ):
        try:
            instance.model_update(update_instance)
            updated_instance = await engine.save(instance)
            return updated_instance
        except (ValidationError, TypeError) as e:
            raise ValidationError(e)

    async def delete(self, instance: ModelType):
        await engine.delete(instance)

    async def find_one(self, filters: dict):
        instance = await self.engine.find_one(self.model, filters)
        if instance:
            return instance
