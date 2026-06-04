import json

import pytest

from app.core.config import settings
from app.db.enums import AlertStatus, Severity
from app.db.models.alert import Alert
from app.services.alert_explanations.providers.openai_provider import (
    OpenAIAlertExplanationProvider,
)


def build_alert() -> Alert:
    return Alert(
        id=1,
        event_id=1,
        title="Anomaly detected: failed_transaction",
        severity=Severity.HIGH,
        status=AlertStatus.OPEN,
        risk_score=90,
        description="AI model detected suspicious transaction behavior.",
    )


def test_openai_provider_requires_api_key(monkeypatch):
    monkeypatch.setattr(settings, "openai_api_key", None)

    with pytest.raises(ValueError) as exc:
        OpenAIAlertExplanationProvider()

    assert "OPENAI_API_KEY is required" in str(exc.value)


def test_openai_provider_returns_expected_response_without_real_api_call(monkeypatch):
    monkeypatch.setattr(settings, "openai_api_key", "test-api-key")
    monkeypatch.setattr(settings, "openai_alert_model", "test-model")

    provider = OpenAIAlertExplanationProvider()

    fake_output = {
        "summary": "Suspicious transaction-related activity was detected.",
        "severity_explanation": "High severity means the alert should be reviewed soon.",
        "possible_causes": [
            "Suspicious transaction behavior.",
            "Unusual user activity.",
            "Possible fraud attempt.",
        ],
        "recommended_actions": [
            "Review related transaction logs.",
            "Check user account activity.",
            "Escalate if similar alerts appear.",
        ],
    }


    class FakeResponse:
        output_text = json.dumps(fake_output)


    class FakeResponses:
        def create(self, model, instructions, input):
            assert model == "test-model"
            assert "cybersecurity assistant" in instructions.lower()
            assert "failed_transaction" in input

            return FakeResponse()


    class FakeClient:
        responses = FakeResponses()

    provider.client = FakeClient()

    result = provider.generate(build_alert())

    assert result["alert_id"] == 1
    assert result["title"] == "Anomaly detected: failed_transaction"
    assert result["severity"] == Severity.HIGH.value
    assert result["status"] == AlertStatus.OPEN.value
    assert result["risk_score"] == 90
    assert result["source"] == "openai"

    assert result["summary"] == fake_output["summary"]
    assert result["severity_explanation"] == fake_output["severity_explanation"]
    assert result["possible_causes"] == fake_output["possible_causes"]
    assert result["recommended_actions"] == fake_output["recommended_actions"]