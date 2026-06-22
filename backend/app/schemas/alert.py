from datetime import datetime
from pydantic import BaseModel
from app.db.enums import AlertStatus, Severity

class AlertUpdateRequest(BaseModel):
    status: AlertStatus

class AlertResponse(BaseModel):
    id: int
    event_id: int
    title: str
    severity: Severity
    status: AlertStatus
    risk_score: int
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}