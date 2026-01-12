from typing import Optional, List
from bson import ObjectId
from datetime import datetime

from app.core.database import get_database
from app.schemas.resolution import ResolutionCreate, ResolutionUpdate


class ResolutionCRUD:
    def __init__(self):
        self.collection_name = "resolutions"

    async def create_resolution(self, resolution_data: ResolutionCreate, user_id: str) -> dict:
        database = await get_database()
        resolution_dict = resolution_data.model_dump()
        resolution_dict["user_id"] = user_id
        resolution_dict["completed"] = False
        resolution_dict["created_at"] = datetime.utcnow()
        resolution_dict["updated_at"] = datetime.utcnow()
        
        result = await database[self.collection_name].insert_one(resolution_dict)
        resolution_dict["_id"] = result.inserted_id
        return resolution_dict

    async def get_resolution_by_id(self, resolution_id: str) -> Optional[dict]:
        database = await get_database()
        resolution = await database[self.collection_name].find_one({"_id": ObjectId(resolution_id)})
        return resolution

    async def get_user_resolutions(self, user_id: str, skip: int = 0, limit: int = 100) -> List[dict]:
        database = await get_database()
        resolutions = await database[self.collection_name].find(
            {"user_id": user_id}
        ).skip(skip).limit(limit).to_list(length=limit)
        return resolutions

    async def update_resolution(self, resolution_id: str, resolution_update: ResolutionUpdate) -> Optional[dict]:
        database = await get_database()
        update_data = resolution_update.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        result = await database[self.collection_name].update_one(
            {"_id": ObjectId(resolution_id)},
            {"$set": update_data}
        )
        
        if result.modified_count:
            return await self.get_resolution_by_id(resolution_id)
        return None

    async def delete_resolution(self, resolution_id: str) -> bool:
        database = await get_database()
        result = await database[self.collection_name].delete_one({"_id": ObjectId(resolution_id)})
        return result.deleted_count > 0

    async def get_all_resolutions(self, skip: int = 0, limit: int = 100) -> List[dict]:
        database = await get_database()
        resolutions = await database[self.collection_name].find().skip(skip).limit(limit).to_list(length=limit)
        return resolutions


resolution_crud = ResolutionCRUD()