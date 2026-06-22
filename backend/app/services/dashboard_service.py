from app.db.enums import AlertStatus, Severity
from app.repositories.alert_repository import AlertRepository
from app.repositories.event_repository import EventRepository


class DashboardService:
    def __init__(
            self,
            alert_repo: AlertRepository,
            event_repo: EventRepository,
    ) -> None:
            self.alert_repo = alert_repo
            self.event_repo = event_repo

    def get_summary(self) -> dict:
          return {
                "total_events": self.event_repo.count_all(),
                "total_alerts": self.alert_repo.count_all(),
                "open_alerts": self.alert_repo.count_by_status(AlertStatus.OPEN),
                "closed_alerts": self.alert_repo.count_by_status(AlertStatus.CLOSED),
                "critical_alerts": self.alert_repo.count_by_severity(Severity.CRITICAL),
                "high_alerts": self.alert_repo.count_by_severity(Severity.HIGH),
                "latest_alerts": self.alert_repo.get_latest(limit=5),

          }        


