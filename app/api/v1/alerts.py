from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies.auth import require_admin
from app.db.session import get_db
from app.db.models.user import User
from app.repositories.alert_repository import AlertRepository
from app.services.alert_service import AlertService
from app.schemas.alert import AlertUpdateRequest, AlertResponse

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("/", response_model=list[AlertResponse])
def list_alerts(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    service = AlertService(AlertRepository(db))
    return service.get_alerts()

@router.patch("/{alert_id}", response_model=AlertResponse)
def update_alert(alert_id: int,
                 payload: AlertUpdateRequest,
                 db: Session = Depends(get_db),
                 _=Depends(require_admin)):
    service = AlertService(AlertRepository(db))
    try:
        return service.update_status(alert_id, payload.status)
    except ValueError:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    

