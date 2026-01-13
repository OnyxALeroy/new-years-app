from typing import Optional, List
from bson import ObjectId
from datetime import datetime

from app.core.database import get_database
from app.core.security import get_password_hash, verify_password
from app.schemas.user import UserCreate, UserUpdate, UserRole


class UserCRUD:
    def __init__(self):
        self.collection_name = "users"

    async def create_user(self, user_data: UserCreate) -> dict:
        database = await get_database()
        user_dict = user_data.model_dump()
        password = user_dict.pop("password")
        # Truncate password to max 72 characters for bcrypt
        user_dict["hashed_password"] = get_password_hash(password[:72])
        user_dict["created_at"] = datetime.utcnow()
        
        result = await database[self.collection_name].insert_one(user_dict)
        user_dict["_id"] = result.inserted_id
        return user_dict

    async def get_user_by_username(self, username: str) -> Optional[dict]:
        database = await get_database()
        user = await database[self.collection_name].find_one({"username": username})
        return user

    async def get_user_by_email(self, email: str) -> Optional[dict]:
        database = await get_database()
        user = await database[self.collection_name].find_one({"email": email})
        return user

    async def get_user_by_id(self, user_id: str) -> Optional[dict]:
        database = await get_database()
        user = await database[self.collection_name].find_one({"_id": ObjectId(user_id)})
        return user

    async def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        user = await self.get_user_by_username(username)
        if not user or not verify_password(password, user["hashed_password"]):
            return None
        return user

    async def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[dict]:
        database = await get_database()
        update_data = user_update.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        result = await database[self.collection_name].update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        if result.modified_count:
            return await self.get_user_by_id(user_id)
        return None

    async def get_users(self, skip: int = 0, limit: int = 100) -> List[dict]:
        database = await get_database()
        users = await database[self.collection_name].find().skip(skip).limit(limit).to_list(length=limit)
        return users

    async def create_admin_user(self):
        admin_exists = await self.get_user_by_username("admin")
        if not admin_exists:
            admin_user = UserCreate(
                username="admin",
                email="admin@newyears.com",
                password="admin123",
                role=UserRole.ADMIN
            )
            await self.create_user(admin_user)


user_crud = UserCRUD()