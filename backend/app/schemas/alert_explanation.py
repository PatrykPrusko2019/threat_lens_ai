from pydantic import BaseModel

class AlertExplanationResponse(BaseModel):
    alert_id: int
    title: str
    severity: str
    risk_score: int
    status: str
    summary: str
    severity_explanation: str
    possible_causes: list[str]
    recommended_actions: list[str]
    source: str = "rule_based"