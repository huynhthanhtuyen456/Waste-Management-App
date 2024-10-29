from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str = Field(..., env='DB_HOST')
    db_user: str = Field(..., env='DB_USER')
    db_password: str = Field(..., env='DB_PASSWORD')
    mongo_db_host: str = Field(..., env='MONGO_DB_HOST')
    mongo_db_user: str = Field(..., env='MONGO_DB_USER')
    mongo_db_password: str = Field(..., env='MONGO_DB_PASSWORD')
    project_name: str = Field(..., env='PROJECT_NAME')
    debug_logs: bool = Field(False, env='DEBUG_LOGS')
    version: str = Field(..., env='VERSION')
    description: str = Field(..., env='DESCRIPTION')

    @property
    def asyncpg_database_url(self):
        return f'postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_user}'

    @property
    def database_psycopg_url(self):
        return f'postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_user}'

    @property
    def mongodb_url(self) -> str:
        replica_set = "?replicaSet=finsc-mongodb&ssl=false" if not self.debug_logs else "?ssl=false"
        return f"mongodb://{self.mongo_db_user}:{self.mongo_db_password}@{self.mongo_db_host}/{replica_set}"


@lru_cache
def get_settings():
    return Settings()
