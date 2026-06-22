from app.db.enums import AlertStatus, Severity
from app.db.models.alert import Alert
from app.services.alert_explanations.providers.rule_based_provider import (
    RuleBasedAlertExplanationProvider,
)

def build_alert(
        title: str = "Anomaly detected: failed_transaction",
        severity: Severity = Severity.HIGH,
        risk_score: int = 90,
        description: str = "AI model detected suspicious transaction behavior.",
) -> Alert:
    return Alert(
        id=1,
        event_id=1,
        title=title,
        severity=severity,
        status=AlertStatus.OPEN,
        risk_score=risk_score,
        description=description,
    )

def test_rule_based_provider_returns_expected_response_contract():
    provider = RuleBasedAlertExplanationProvider()
    alert = build_alert()

    result = provider.generate(alert)

    assert result["alert_id"] == 1
    assert result["title"] == alert.title
    assert result["severity"] == Severity.HIGH.value
    assert result["risk_score"] == 90
    assert result["status"] == AlertStatus.OPEN.value
    assert result["source"] == "rule_based"

    assert isinstance(result["summary"], str)
    assert isinstance(result["severity_explanation"], str)
    assert isinstance(result["possible_causes"], list)
    assert isinstance(result["recommended_actions"], list)

def test_high_severity_alert_uses_high_severity_explanation():
    provider = RuleBasedAlertExplanationProvider()
    alert = build_alert(severity=Severity.HIGH, risk_score=90)

    result = provider.generate(alert)

    assert result["severity_explanation"].startswith("High severity")

def test_transaction_alert_returns_transaction_related_causes():
    provider = RuleBasedAlertExplanationProvider()
    alert = build_alert(
        title="Anomaly detected: failed_transaction",
        description="Suspicious transaction behavior detected.",
    )

    result = provider.generate(alert)

    assert "Suspicious transaction behavior." in result["possible_causes"]

def test_autoencoder_alert_returns_network_anomaly_causes():
    provider = RuleBasedAlertExplanationProvider()
    alert = build_alert(
        title="Autoencoder network anomaly detected",
        severity=Severity.MEDIUM,
        risk_score=45,
        description="Potential anomalous network behavior detected by Autoencoder model."
    )

    result = provider.generate(alert)

    assert (
        "Unusual network traffic pattern compared to learned normal behavior."
        in result["possible_causes"]
    )
    assert result["severity_explanation"].startswith("Medium severity")            