from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user, require_admin
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
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    service = EventService(EventRepository(db))
    return service.get_events()