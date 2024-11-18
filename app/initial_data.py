import asyncio
import logging
import os
from enum import Enum

from passlib.context import CryptContext
from pymongo import MongoClient
from pymongo.server_api import ServerApi


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1

mongodb_url = (f'mongodb://{os.environ["MONGO_DB_USER"]}:{os.environ["MONGO_DB_PASSWORD"]}@'
               f'{os.environ["MONGO_DB_HOST"]}?ssl=false')
client = MongoClient(mongodb_url, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = client.waste_management_db
user_collections = db["user"]
score_rank_collections = db["score_rank"]
permission_collections = db["permission"]
role_collections = db["role"]
category_collection = db["waste_category"]
instruction_type_collection = db["waste_instruction_type"]
instruction_collection = db["waste_instruction"]
scoring_criteria_collection = db["scoring_criteria"]
challenge_collection = db["challenge"]


class ScoreRankEnum(str, Enum):
    Platinum = "Platinum"
    Gold = "Gold"
    Silver = "Silver"
    Bronze = "Bronze"


async def populate_db() -> None:
    rank_list = [
        {
            "score": 10,
            "level": ScoreRankEnum.Bronze
        },
        {
            "score": 20,
            "level": ScoreRankEnum.Silver
        },
        {
            "score": 30,
            "level": ScoreRankEnum.Gold
        },
        {
            "score": 40,
            "level": ScoreRankEnum.Platinum
        },
    ]
    ranks = score_rank_collections.find({"level": {"$in": [rank["level"] for rank in rank_list]}})
    ranks = [rank for rank in ranks]
    if not ranks:
        score_rank_collections.insert_many(rank_list)

    permissions_list = [
        {
            "name": "create",
            "description": "Can create documents in database"
        },
        {
            "name": "update",
            "description": "Can update documents in database"
        },
        {
            "name": "get",
            "description": "Can get documents in database"
        },
        {
            "name": "delete",
            "description": "Can delete documents in database"
        },
        {
            "name": "create_waste",
            "description": "Can create documents in database"
        },
        {
            "name": "update_waste",
            "description": "Can update documents in database"
        },
        {
            "name": "get_waste",
            "description": "Can get documents in database"
        },
    ]
    permissions = role_collections.find({"name": {"$in": [permission["name"] for permission in permissions_list]}})
    permissions = [perm for perm in permissions]
    if not permissions:
        permission_collections.insert_many(permissions_list)

    roles = role_collections.find({"name": {"$in": ["Admin", "Member", "Moderator"]}})
    roles = [role for role in roles]
    if not roles:
        roles = [
            {
                "name": "Admin",
                "description": "Administrator",
                "permission_ids": [perm["_id"] for perm in permission_collections.find({})]
            },
            {
                "name": "Member",
                "description": "Member",
                "permission_ids": [
                    perm["_id"] for perm in permission_collections.find({})
                    if perm["name"] in ["create_waste", "get_waste", "update_waste"]
                ]
            },
            {
                "name": "Moderator",
                "description": "Moderator",
                "permission_ids": [perm["_id"] for perm in permission_collections.find({}) if perm["name"] != "delete"]
            },
        ]
        role_collections.insert_many(roles)

    user = user_collections.find_one({"email": os.environ["FIRST_SUPERUSER"]})
    if not user:
        role = role_collections.find_one({"name": "Admin"})
        user_collections.insert_one({
            "email": os.environ["FIRST_SUPERUSER"],
            "first_name": "Super",
            "last_name": "User",
            "hashed_password": pwd_context.hash(os.environ["FIRST_SUPERUSER_PASSWORD"]),
            "is_active": True,
            "score": 0,
            "role": role["_id"],
        })

    dump_scoring_criteria = [
        {
            "criteria": "Food scraps, vegetable peels.",
            "score": 2,
        },
        {
            "criteria": "Paper, cardboard, glass bottles, cans.",
            "score": 1,
        },
        {
            "criteria": "Hazardous items.",
            "score": 5,
        },
    ]
    scoring_criteria = scoring_criteria_collection.find(
        {"criteria": {"$in": [item["criteria"] for item in dump_scoring_criteria]}})
    scoring_criteria = [scoring for scoring in scoring_criteria]
    if not scoring_criteria:
        scoring_criteria_collection.insert_many(dump_scoring_criteria)

    dump_challenges = [
        {
            "name": "Sort the Kitchen Waste",
            "description": "Sort a list of common kitchen waste items into the organic category.",
            "difficulty_level": 2,
            "scoring_criteria": [
                item["_id"] for item in scoring_criteria_collection.find({"criteria": "Food scraps, vegetable peels."})
            ]
        },
        {
            "name": "Identify Misplaced Items",
            "description": "Categorize plastic in you home trash bin.",
            "difficulty_level": 1,
            "scoring_criteria": [
                item["_id"] for item in
                scoring_criteria_collection.find({"criteria": "Paper, cardboard, glass bottles, cans."})
            ]
        },
        {
            "name": "Hazardous Waste Cleanup",
            "description": "Identify hazardous waste items from a mixed waste pile and separate them for proper disposal.",
            "difficulty_level": 4,
            "scoring_criteria": [
                item["_id"] for item in scoring_criteria_collection.find({"criteria": "Hazardous items."})
            ]
        },
    ]
    challenges = challenge_collection.find({"name": {"$in": [item["name"] for item in dump_challenges]}})
    challenges = [item for item in challenges]
    if not challenges:
        challenge_collection.insert_many(dump_challenges)

    dump_categories = [
        {
            "name": "Organic Waste",
            "description": "Any material that is biodegradable and comes from either a plant or an animal. For example, food scraps, yard waste, coffee grounds, and eggshells.",
            "challenges": [
                item
                for item in challenge_collection.find({"name": {"$in": [item["name"] for item in dump_challenges[:1]]}})
            ]
        },
        {
            "name": "Recyclable Waste",
            "description": "Waste that can be processed and reused to create new materials and objects. For example, paper, cardboard, glass bottles, cans, and plastics.",
            "challenges": [item for item in challenge_collection.find({"name": {"$in": [item["name"] for item in dump_challenges]}})]
        },
        {
            "name": "Hazardous Waste",
            "description": "Waste that can be dangerous to people or the environment if not handled and disposed of properly, for example, batteries, paint, chemicals, fluorescent bulbs, and electronics.",
            "challenges": [item for item in challenge_collection.find({"name": {"$in": [dump_challenges[0]["name"]]}})]
        },
    ]
    categories = category_collection.find({"name": {"$in": [item["name"] for item in dump_categories]}})
    categories = [cat for cat in categories]
    if not categories:
        category_collection.insert_many(dump_categories)

    dump_instruction_type = [
        {
            "type": "Disposal",
            "description": "Waste Disposal",
        },
        {
            "type": "Classification",
            "description": "How to classify waste",
        },
    ]
    instruction_types = instruction_type_collection.find({"type": {"$in": [item["type"] for item in dump_instruction_type]}})
    instruction_types = [instruction_type for instruction_type in instruction_types]
    if not instruction_types:
        instruction_type_collection.insert_many(dump_instruction_type)

    dump_disposal_instructions = [
        {
            "title": "Composting",
            "content": "- Compost at home or drop off at a local composting facility.\n"
                           "- Avoid mixing with non-compostable materials like plastic.",
        },
        {
            "title": "Cleaning food items",
            "content": "Rinse and clean items to remove food residue.",
        },
        {
            "title": "Disposal Cautions",
            "content": "- Do not throw in regular trash bins.",
        },
        {
            "title": "Local Guidelines",
            "content": "- Take to a designated hazardous waste disposal facility.\n"
                           "- Follow special storage guidelines to prevent leaks or contamination.",
        },
    ]
    dump_classification_instructions = [
        {
            "title": "Classification",
            "content": "- Separate materials by type (e.g., paper, glass, metal).\n"
                           "- Follow your local recycling guidelines to determine what is accepted.",
        }
    ]
    instructions = instruction_collection.find({"title": {"$in": [item["title"] for item in dump_disposal_instructions]}})
    instructions = [instruction for instruction in instructions]
    if not instructions:
        instruction_type = instruction_type_collection.find_one({"type": "Disposal"})
        category = category_collection.find_one({"name": "Hazardous Waste"})
        inserted_many = []
        for instruction in dump_disposal_instructions:
            instruction["type"] = instruction_type["_id"]
            instruction["category"] = category["_id"]
            inserted_many.append(instruction)
        instruction_collection.insert_many(inserted_many)

    classification_instructions = instruction_collection.find({"title": {"$in": [item["title"] for item in dump_classification_instructions]}})
    classification_instructions = [instruction for instruction in classification_instructions]
    if not classification_instructions:
        instruction_type = instruction_type_collection.find_one({"type": "Classification"})
        category = category_collection.find_one({"name": "Recyclable Waste"})
        inserted_many = []
        for instruction in dump_classification_instructions:
            instruction["type"] = instruction_type["_id"]
            instruction["category"] = category["_id"]
            inserted_many.append(instruction)
        instruction_collection.insert_many(inserted_many)


async def main() -> None:
    logger.info("Creating initial data")
    await populate_db()
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())