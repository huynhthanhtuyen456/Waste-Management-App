from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_db_host: str = Field(...)
    mongo_db_user: str = Field(...)
    mongo_db_password: str = Field(...)
    mongo_db: str = Field(...)
    project_name: str = Field(...)
    debug_logs: bool = Field(False)
    version: str = Field(...)
    description: str = Field(...)
    secret_key: str = Field(...)
    algorithm: str = Field(...)
    access_token_expire_minutes: int = Field(...)
    first_superuser: str = Field(...)
    first_superuser_password: str = Field(...)
    page_limit: int = Field(...)

    @property
    def mongodb_url(self) -> str:
        return f"mongodb://{self.mongo_db_user}:{self.mongo_db_password}@{self.mongo_db_host}?ssl=false"


@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
