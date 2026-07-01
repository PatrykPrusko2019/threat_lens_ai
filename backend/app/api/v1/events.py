from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.db.models.user import User
from app.db.session import get_db
from app.repositories.event_repository import EventRepository
from app.schemas.event import EventCreate, EventResponse
from app.services.event_service import EventService

router = APIRouter(prefix="/events", tags=["events"])

@router.post("/", response_model=EventResponse)
def create_event(
    payload: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = EventService(EventRepository(db))
    return service.create_event(payload, current_user.id)

@router.get("/", response_model=list[EventResponse])
def list_events(
    event_type: str | None = None,
    severity: str | None = None,
    source_ip: str | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    service = EventService(EventRepository(db))

    return service.get_events(
        event_type=event_type,
        severity=severity,
        source_ip=source_ip,
        limit=limit,
    )

@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    service = EventService(EventRepository(db))

    try:
        return service.get_event_by_id(event_id)
    
    except ValueError:
        raise HTTPException(status_code=404, detail="Event not found")