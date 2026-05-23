from app.repositories.alert_repository import AlertRepository
from app.services.alert_explanations.providers.base import AlertExplanationProvider
from app.services.alert_explanations.providers.rule_based_provider import (
    RuleBasedAlertExplanationProvider,
)

class AlertExplanationService:
    def __init__(
            self,
            alert_repo: AlertRepository,
            provider: AlertExplanationProvider | None = None,
    ) -> None:
        self.alert_repo = alert_repo
        self.provider = provider or RuleBasedAlertExplanationProvider()

    def explain_alert(self, alert_id: int) -> dict:
        alert = self.alert_repo.get_by_id(alert_id)

        if not alert:
            raise ValueError("Alert not found")
        
        return self.provider.generate(alert)