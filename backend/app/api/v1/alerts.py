from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies.auth import require_admin
from app.db.session import get_db
from app.db.models.user import User
from app.repositories.alert_repository import AlertRepository
from app.services.alert_service import AlertService
from app.services.alert_explanations.alert_explanation_service import AlertExplanationService
from app.schemas.alert import AlertUpdateRequest, AlertResponse
from app.schemas.alert_explanation import AlertExplanationResponse

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("/", response_model=list[AlertResponse])
def list_alerts(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    service = AlertService(AlertRepository(db))
    return service.get_alerts()

@router.post("/{alert_id}/explain", response_model=AlertExplanationResponse)
def explain_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    service = AlertExplanationService(AlertRepository(db))

    try:
        return service.explain_alert(alert_id)
    
    except ValueError:
        raise HTTPException(status_code=404, detail="Alert not found")
    

@router.patch("/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: int,
    payload: AlertUpdateRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    service = AlertService(AlertRepository(db))
    
    try:
        return service.update_status(alert_id, payload.status)
    
    except ValueError:
        raise HTTPException(status_code=404, detail="Alert not found")