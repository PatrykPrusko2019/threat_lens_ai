from datetime import datetime

from pydantic import BaseModel

class AlertResponse(BaseModel):
    id: int
    event_id: int
    title: str
    severity: str
    status: str
    risk_score: int
    description: str | None
    created_at: datetime

    model_config = {"from_attributes": True}