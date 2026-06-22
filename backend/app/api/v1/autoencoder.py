from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies.auth import require_admin
from app.db.session import get_db
from app.repositories.alert_repository import AlertRepository
from app.repositories.event_repository import EventRepository
from app.schemas.autoencoder import AutoencoderResponse
from app.schemas.network_event import NetworkEventRequest
from app.services.autoencoder_service import AutoencoderService

router = APIRouter(
    prefix="/autoencoder",
    tags=["autoencoder"],
)

@router.post(
    "/check",
    response_model=AutoencoderResponse,
)
def check_autoencoder(
    payload: NetworkEventRequest,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    service = AutoencoderService(
        event_repo=EventRepository(db),
        alert_repo=AlertRepository(db),
    )

    try:
        return service.check_anomaly(payload)
    
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )