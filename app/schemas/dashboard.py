from pydantic import BaseModel

from app.schemas.alert import AlertResponse


class DashboardSummaryResponse(BaseModel):
    total_events: int
    total_alerts: int
    open_alerts: int
    closed_alerts: int
    critical_alerts: int
    high_alerts: int
    latest_alerts: list[AlertResponse]