from app.config import get_settings
from motor import motor_asyncio, core
from odmantic import AIOEngine
from pymongo.driver_info import DriverInfo

DRIVER_INFO = DriverInfo(name="waste-management-application", version=get_settings().version)


class _MongoClientSingleton:
    instance = None
    mongo_client: motor_asyncio.AsyncIOMotorClient | None
    engine: AIOEngine

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(_MongoClientSingleton, cls).__new__(cls)
            cls.instance.mongo_client = motor_asyncio.AsyncIOMotorClient(
                get_settings().mongodb_url, driver=DRIVER_INFO
            )
            cls.instance.engine = AIOEngine(client=cls.instance.mongo_client, database=get_settings().mongo_db)
        return cls.instance


def get_mongo_database() -> core.AgnosticDatabase:
    return _MongoClientSingleton().mongo_client[get_settings().mongo_db]


def get_engine() -> AIOEngine:
    return _MongoClientSingleton().engine


async def ping():
    await get_mongo_database().command("ping")


engine = get_engine()
__all__ = ["get_mongo_database", "ping", "engine"]