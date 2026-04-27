from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies.auth import require_admin
from app.db.session import get_db
from app.repositories.event_repository import EventRepository
from app.repositories.alert_repository import AlertRepository
from app.schemas.fraud import FraudRequest
from app.services.fraud_service import FraudService

router = APIRouter(prefix="/fraud", tags=["fraud"])

@router.post("/check")
def check_fraud(
    payload: FraudRequest,
    db: Session = Depends(get_db),
    _=Depends(require_admin),
):
    service = FraudService(
        event_repo=EventRepository(db),
        alert_repo=AlertRepository(db),
    )
    return service.check_transaction(payload.features)

