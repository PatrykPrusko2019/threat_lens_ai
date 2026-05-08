from pydantic import BaseModel

class AutoencoderResponse(BaseModel):
    anomaly: bool
    anomaly_score: float
    raw_anomaly_score: float
    reconstruction_error: float
    threshold: float