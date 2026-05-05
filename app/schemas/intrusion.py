from pydantic import BaseModel, Field

class IntrusionCheckRequest(BaseModel):
    features: list[float] = Field(min_length=57, max_length=57)


class IntrusionCheckResponse(BaseModel):
    intrusion: bool
    attack_probability: float
    event_id: int | None = None
    alert_id: int | None = None
        