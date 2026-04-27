from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth import require_admin
from app.db.session import get_db
from app.db.models.user import User
from app.repositories.alert_repository import AlertRepository
from app.schemas.alert import AlertResponse
from app.services.alert_service import AlertService

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("/", response_model=list[AlertResponse])
def list_alerts(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    service = AlertService(AlertRepository(db))
    return service.get_alerts()
