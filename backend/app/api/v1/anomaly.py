from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.db.session import get_db
from app.repositories.alert_repository import AlertRepository
from app.repositories.event_repository import EventRepository
from app.services.anomaly_service import AnomalyService

router = APIRouter(prefix="/anomaly", tags=["anomaly"])

@router.get("/")
def detect_anomalies(
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    service = AnomalyService(
        event_repo=EventRepository(db),
        alert_repo=AlertRepository(db),
    )
    return service.analyze()
