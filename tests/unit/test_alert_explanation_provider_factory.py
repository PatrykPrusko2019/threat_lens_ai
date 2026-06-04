import pytest

from app.core.config import settings
from app.services.alert_explanations.provider_factory import (
    get_alert_explanation_provider,
)
from app.services.alert_explanations.providers.openai_provider import (
    OpenAIAlertExplanationProvider,
)
from app.services.alert_explanations.providers.rule_based_provider import (
    RuleBasedAlertExplanationProvider,
)


def test_provider_factory_returns_rule_based_provider(monkeypatch):
    monkeypatch.setattr(settings, "alert_explanation_provider", "rule_based")

    provider = get_alert_explanation_provider()

    assert isinstance(provider, RuleBasedAlertExplanationProvider)


def test_provider_factory_returns_openai_provider(monkeypatch):
    monkeypatch.setattr(settings, "alert_explanation_provider", "openai")
    monkeypatch.setattr(settings, "openai_api_key", "test-api-key")

    provider = get_alert_explanation_provider()

    assert isinstance(provider, OpenAIAlertExplanationProvider)


def test_provider_factory_rejects_unknown_provider(monkeypatch):
    monkeypatch.setattr(settings, "alert_explanation_provider", "unknown_provider")

    with pytest.raises(ValueError) as exc:
        get_alert_explanation_provider()

    assert "Unsupported alert explanation provider" in str(exc.value)