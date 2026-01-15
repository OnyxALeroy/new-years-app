from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Participant(BaseModel):
    user_id: str
    tags: List[str] = Field(
        default_factory=list, description="e.g., ['vegan', 'halal']"
    )
    due_payment: float = Field(default=0.0, ge=0)
    paid_amount: float = Field(default=0.0, ge=0)


class EventBase(BaseModel):
    organizers: List[str] = Field(description="At least one organizer required")
    locations: List[str] = Field(description="At least one location required")
    description: str
    dates: List[datetime] = Field(description="Event dates (at least one required)")
    images: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)


class EventCreate(EventBase):
    participants: List[Participant] = Field(default_factory=list)


class EventUpdate(BaseModel):
    organizers: Optional[List[str]] = None
    locations: Optional[List[str]] = None
    description: Optional[str] = None
    dates: Optional[List[datetime]] = None
    images: Optional[List[str]] = None
    notes: Optional[List[str]] = None
    participants: Optional[List[Participant]] = None


class EventInDB(EventBase):
    id: str
    participants: List[Participant]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EventResponse(BaseModel):
    id: str
    organizers: List[str]
    locations: List[str]
    description: str
    dates: List[datetime]
    images: List[str]
    notes: List[str]
    participants: List[Participant]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
