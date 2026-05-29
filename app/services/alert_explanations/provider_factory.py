from app.core.config import settings
from app.services.alert_explanations.providers.base import AlertExplanationProvider
from app.services.alert_explanations.providers.rule_based_provider import (
    RuleBasedAlertExplanationProvider,
)

def get_alert_explanation_provider() -> AlertExplanationProvider:
    provider_name = settings.alert_explanation_provider.lower()

    if provider_name == "rule_based":
        return RuleBasedAlertExplanationProvider()

    raise ValueError(f"Unsupported alert explanation provider: {provider_name}") 
