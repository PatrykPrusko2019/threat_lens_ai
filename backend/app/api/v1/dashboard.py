from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.db.models.user import User
from app.db.session import get_db
from app.repositories.alert_repository import AlertRepository
from app.repositories.event_repository import EventRepository
from app.schemas.dashboard import DashboardSummaryResponse
from app.services.dashboard_service import DashboardService


router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    service = DashboardService(
        alert_repo=AlertRepository(db),
        event_repo=EventRepository(db),
    )

    return service.get_summary()