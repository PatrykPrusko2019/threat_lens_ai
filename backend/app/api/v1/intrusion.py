from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth import require_admin
from app.db.session import get_db
from app.repositories.alert_repository import AlertRepository
from app.repositories.event_repository import EventRepository
from app.schemas.intrusion import IntrusionCheckResponse
from app.schemas.network_event import NetworkEventRequest
from app.services.intrusion_service import IntrusionService

router = APIRouter(prefix="/intrusion", tags=["intrusion"])

@router.post("/check", response_model=IntrusionCheckResponse)
def check_intrusion(
    payload: NetworkEventRequest,
    db: Session = Depends(get_db),
    _=Depends(require_admin)
):
    service = IntrusionService(
        event_repo=EventRepository(db),
        alert_repo=AlertRepository(db)
    )

    try:
        return service.check_intrusion(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))