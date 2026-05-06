from pydantic import BaseModel, Field

class IntrusionCheckRequest(BaseModel):
    features: dict[str, float] = Field(description="Dictionary with CICIDS feature names as keys")


class IntrusionCheckResponse(BaseModel):
    intrusion: bool
    attack_probability: float
    event_id: int | None = None
    alert_id: int | None = None
        