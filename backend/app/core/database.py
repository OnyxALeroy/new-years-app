from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings


class Database:
    client: Any = None
    database: Any = None


db = Database()


async def get_database():
    if db.database is None:
        raise ValueError("Database not connected. Call connect_to_mongo() first.")
    return db.database


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.DATABASE_URL)
    db.database = db.client.get_database()


async def close_mongo_connection():
    if db.client:
        db.client.close()
