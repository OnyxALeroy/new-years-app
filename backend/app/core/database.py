from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings


class Database:
    client: AsyncIOMotorClient = None
    database = None


db = Database()


async def get_database():
    return db.database


async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.DATABASE_URL)
    db.database = db.client.get_database()


async def close_mongo_connection():
    db.client.close()