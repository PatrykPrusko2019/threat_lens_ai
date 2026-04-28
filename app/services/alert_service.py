from app.db.models.alert import Alert
from app.repositories.alert_repository import AlertRepository
from app.db.enums import AlertStatus


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
    
    def update_status(self, alert_id: int, status: AlertStatus):
        alert = self.repo.get_by_id(alert_id)
        if not alert:
            raise ValueError("Alert not found")
        
        alert.status = status
        return self.repo.save(alert)