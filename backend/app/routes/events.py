from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional

from app.routes.auth import get_current_user_auth, get_admin_user
from app.crud.event import event_crud
from app.schemas.event import EventCreate, EventUpdate, EventResponse, Participant

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventResponse)
async def create_event(
    event: EventCreate,
    current_user: dict = Depends(get_current_user_auth)
):
    db_event = await event_crud.create_event(event)
    return EventResponse(
        id=str(db_event["_id"]),
        organizers=db_event["organizers"],
        locations=db_event["locations"],
        description=db_event["description"],
        dates=db_event["dates"],
        images=db_event["images"],
        notes=db_event["notes"],
        participants=[
            Participant(**participant) for participant in db_event["participants"]
        ],
        created_at=db_event["created_at"],
        updated_at=db_event.get("updated_at")
    )


@router.get("/", response_model=list[EventResponse])
async def get_events(
    skip: int = 0,
    limit: int = 100,
    organizer: Optional[str] = None,
    location: Optional[str] = None
):
    if organizer:
        events = await event_crud.get_events_by_organizer(organizer, skip, limit)
    elif location:
        events = await event_crud.get_events_by_location(location, skip, limit)
    else:
        events = await event_crud.get_events(skip, limit)
    
    return [
        EventResponse(
            id=str(event["_id"]),
            organizers=event["organizers"],
            locations=event["locations"],
            description=event["description"],
            dates=event["dates"],
            images=event["images"],
            notes=event["notes"],
            participants=[
                Participant(**participant) for participant in event["participants"]
            ],
            created_at=event["created_at"],
            updated_at=event.get("updated_at")
        )
        for event in events
    ]


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: str):
    event = await event_crud.get_event_by_id(event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    return EventResponse(
        id=str(event["_id"]),
        organizers=event["organizers"],
        locations=event["locations"],
        description=event["description"],
        dates=event["dates"],
        images=event["images"],
        notes=event["notes"],
        participants=[
            Participant(**participant) for participant in event["participants"]
        ],
        created_at=event["created_at"],
        updated_at=event.get("updated_at")
    )


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: str,
    event_update: EventUpdate,
    current_user: dict = Depends(get_current_user_auth)
):
    updated_event = await event_crud.update_event(event_id, event_update)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    return EventResponse(
        id=str(updated_event["_id"]),
        organizers=updated_event["organizers"],
        locations=updated_event["locations"],
        description=updated_event["description"],
        dates=updated_event["dates"],
        images=updated_event["images"],
        notes=updated_event["notes"],
        participants=[
            Participant(**participant) for participant in updated_event["participants"]
        ],
        created_at=updated_event["created_at"],
        updated_at=updated_event.get("updated_at")
    )


@router.delete("/{event_id}")
async def delete_event(
    event_id: str,
    current_user: dict = Depends(get_admin_user)
):
    success = await event_crud.delete_event(event_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    return {"message": "Event deleted successfully"}


@router.post("/{event_id}/participants", response_model=EventResponse)
async def add_participant(
    event_id: str,
    participant: Participant,
    current_user: dict = Depends(get_current_user_auth)
):
    updated_event = await event_crud.add_participant(event_id, participant)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    
    return EventResponse(
        id=str(updated_event["_id"]),
        organizers=updated_event["organizers"],
        locations=updated_event["locations"],
        description=updated_event["description"],
        dates=updated_event["dates"],
        images=updated_event["images"],
        notes=updated_event["notes"],
        participants=[
            Participant(**participant) for participant in updated_event["participants"]
        ],
        created_at=updated_event["created_at"],
        updated_at=updated_event.get("updated_at")
    )


@router.delete("/{event_id}/participants/{user_id}", response_model=EventResponse)
async def remove_participant(
    event_id: str,
    user_id: str,
    current_user: dict = Depends(get_current_user_auth)
):
    updated_event = await event_crud.remove_participant(event_id, user_id)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found or participant not in event"
        )
    
    return EventResponse(
        id=str(updated_event["_id"]),
        organizers=updated_event["organizers"],
        locations=updated_event["locations"],
        description=updated_event["description"],
        dates=updated_event["dates"],
        images=updated_event["images"],
        notes=updated_event["notes"],
        participants=[
            Participant(**participant) for participant in updated_event["participants"]
        ],
        created_at=updated_event["created_at"],
        updated_at=updated_event.get("updated_at")
    )


@router.patch("/{event_id}/participants/{user_id}/payment", response_model=EventResponse)
async def update_participant_payment(
    event_id: str,
    user_id: str,
    paid_amount: float,
    current_user: dict = Depends(get_current_user_auth)
):
    if paid_amount < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Paid amount cannot be negative"
        )
    
    updated_event = await event_crud.update_participant_payment(event_id, user_id, paid_amount)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found or participant not in event"
        )
    
    return EventResponse(
        id=str(updated_event["_id"]),
        organizers=updated_event["organizers"],
        locations=updated_event["locations"],
        description=updated_event["description"],
        dates=updated_event["dates"],
        images=updated_event["images"],
        notes=updated_event["notes"],
        participants=[
            Participant(**participant) for participant in updated_event["participants"]
        ],
        created_at=updated_event["created_at"],
        updated_at=updated_event.get("updated_at")
    )