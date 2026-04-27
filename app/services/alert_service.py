from app.db.models.alert import Alert
from app.repositories.alert_repository import AlertRepository


class AlertService:
    def __init__(self, repo: AlertRepository) -> None:
        self.repo = repo

    def create_alert(
            self,
            event_id: int,
            title: str,
            severity: str,
            risk_score: int,
            description: str | None = None,
    )    -> Alert:
        alert = Alert(
            event_id=event_id,
            title=title,
            severity=severity,
            risk_score=risk_score,
            description=description
        )
        return self.repo.create(alert)
    
    def get_alerts(self) -> list[Alert]:
        return self.repo.get_all()