from pydantic import BaseModel

class FraudRequest(BaseModel):
    features: list[float]