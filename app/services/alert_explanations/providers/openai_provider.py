import json

from openai import OpenAI

from app.core.config import settings
from app.db.models.alert import Alert
from app.services.alert_explanations.providers.base import AlertExplanationProvider


class OpenAIAlertExplanationProvider(AlertExplanationProvider):
    source = "openai"

    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAI alert explanations")
        
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_alert_model


    def generate(self, alert: Alert) -> dict:
        prompt = self._build_prompt(alert)

        response = self.client.responses.create(
            model=self.model,
            instructions=(
                "You are a cybersecurity assistant. "
                "Return only valid JSON. Do not incude markdown."
            ),
            input=prompt,
        )

        data = json.loads(response.output_text)

        return {
            "alert_id": alert.id,
            "title": alert.title,
            "severity": self._to_str(alert.severity),
            "risk_score": alert.risk_score,
            "status": self._to_str(alert.status),
            "summary": data["summary"],
            "severity_explanation": data["severity_explanation"],
            "possible_causes": data["possible_causes"],
            "recommended_actions": data["recommended_actions"],
            "source": self.source,
        }


    def _build_prompt(self, alert: Alert) -> str:
        return f"""
Generate a concise cybersecurity alert explanation.str

Alert data:
- Title: {alert.title}
- Severity: {self._to_str(alert.severity)}
- Risk score: {alert.risk_score}
- Status: {self._to_str(alert.status)}
- Description: {alert.description or "No description available"}

Return JSON with exactly these fields:
{{
    "summary": "short explanation of what happened",
    "severity_explanation": "why this severity matters",
    "possible_causes": ["cause 1", "cause 2", "cause 3"],
    "recommended_actions": ["action 1", "action 2", "action 3"]
}}
""".strip()
    

    def _to_str(self, value) -> str:
        if hasattr(value, "value"):
            return value.value
        
        return str(value)