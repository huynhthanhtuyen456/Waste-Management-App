import logging
import sys

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.config.prod import get_settings

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if get_settings().debug_logs else logging.INFO)
logger = logging.getLogger(__name__)

# Heavily inspired by https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html
# Create a new client and connect to the server
client = MongoClient(get_settings().mongodb_url, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection

db = client.admin
collection = db["dividend_events"]

try:
    client.admin.command('ping')
    logger.info("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    logger.error(e)