import logging
import sys

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from app.config import get_settings

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if get_settings().debug_logs else logging.INFO)
logger = logging.getLogger(__name__)

# Heavily inspired by https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html
# Create a new client and connect to the server
# Send a ping to confirm a successful connection
client = AsyncIOMotorClient(get_settings().mongodb_url)
engine = AIOEngine(client=client, database="waste_management_db")


try:
    client.admin.command('ping')
    logger.info("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    logger.error(e)