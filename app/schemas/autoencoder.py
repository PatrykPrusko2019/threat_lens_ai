from pydantic import BaseModel

class AutoencoderResponse(BaseModel):
    anomaly: bool
    anomaly_score: float
    raw_anomaly_score: float
    reconstruction_error: float
    threshold: float
    severity: str | None = None
    risk_score: int | None = None
    event_id: int | None = None
    alert_id: int | None = None