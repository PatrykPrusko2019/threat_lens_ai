from pydantic import BaseModel, Field

class FraudRequest(BaseModel):
    features: list[float] = Field(min_length=30, max_length=30)