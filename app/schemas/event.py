from datetime import datetime
from pydantic import BaseModel

class EventCreate(BaseModel):
    event_type: str
    severity: str
    source_ip: str | None = None
    description: str | None = None


class EventResponse(BaseModel):
    id: int
    event_type: str
    severity: str
    source_ip: str | None
    user_id: int | None
    description: str | None
    created_at: datetime

    model_config = {"from_attributes": True}    