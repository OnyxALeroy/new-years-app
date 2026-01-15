from typing import Optional, List
from bson import ObjectId
from datetime import datetime

from app.core.database import get_database
from app.schemas.event import EventCreate, EventUpdate, Participant


class EventCRUD:
    def __init__(self):
        self.collection_name = "events"

    async def create_event(self, event_data: EventCreate) -> dict:
        database = await get_database()
        event_dict = event_data.model_dump()
        event_dict["created_at"] = datetime.utcnow()
        
        result = await database[self.collection_name].insert_one(event_dict)
        event_dict["_id"] = result.inserted_id
        return event_dict

    async def get_event_by_id(self, event_id: str) -> Optional[dict]:
        database = await get_database()
        event = await database[self.collection_name].find_one({"_id": ObjectId(event_id)})
        return event

    async def get_events(self, skip: int = 0, limit: int = 100) -> List[dict]:
        database = await get_database()
        events = await database[self.collection_name].find().skip(skip).limit(limit).to_list(length=limit)
        return events

    async def get_events_by_organizer(self, organizer: str, skip: int = 0, limit: int = 100) -> List[dict]:
        database = await get_database()
        events = await database[self.collection_name].find({"organizers": organizer}).skip(skip).limit(limit).to_list(length=limit)
        return events

    async def get_events_by_location(self, location: str, skip: int = 0, limit: int = 100) -> List[dict]:
        database = await get_database()
        events = await database[self.collection_name].find({"locations": location}).skip(skip).limit(limit).to_list(length=limit)
        return events

    async def update_event(self, event_id: str, event_update: EventUpdate) -> Optional[dict]:
        database = await get_database()
        update_data = event_update.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        
        result = await database[self.collection_name].update_one(
            {"_id": ObjectId(event_id)},
            {"$set": update_data}
        )
        
        if result.modified_count:
            return await self.get_event_by_id(event_id)
        return None

    async def add_participant(self, event_id: str, participant: Participant) -> Optional[dict]:
        database = await get_database()
        
        result = await database[self.collection_name].update_one(
            {"_id": ObjectId(event_id)},
            {
                "$push": {"participants": participant.model_dump()},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        if result.modified_count:
            return await self.get_event_by_id(event_id)
        return None

    async def remove_participant(self, event_id: str, user_id: str) -> Optional[dict]:
        database = await get_database()
        
        result = await database[self.collection_name].update_one(
            {"_id": ObjectId(event_id)},
            {
                "$pull": {"participants": {"user_id": user_id}},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        if result.modified_count:
            return await self.get_event_by_id(event_id)
        return None

    async def update_participant_payment(self, event_id: str, user_id: str, paid_amount: float) -> Optional[dict]:
        database = await get_database()
        
        result = await database[self.collection_name].update_one(
            {"_id": ObjectId(event_id), "participants.user_id": user_id},
            {
                "$set": {
                    "participants.$.paid_amount": paid_amount,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.modified_count:
            return await self.get_event_by_id(event_id)
        return None

    async def delete_event(self, event_id: str) -> bool:
        database = await get_database()
        result = await database[self.collection_name].delete_one({"_id": ObjectId(event_id)})
        return result.deleted_count > 0


event_crud = EventCRUD()