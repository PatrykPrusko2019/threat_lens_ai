from sqlalchemy.orm import Session

from app.db.enums import AlertStatus, Severity
from app.db.models.alert import Alert

class AlertRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, alert: Alert) -> Alert:
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def get_all(self) -> list[Alert]:
        return self.db.query(Alert).all()    
    
    def get_by_id(self, alert_id: int) -> Alert | None:
        return self.db.query(Alert).filter(Alert.id == alert_id).first()
    
    def get_latest(self, limit: int = 5) -> list[Alert]:
        return (
            self.db.query(Alert)
            .order_by(Alert.created_at.desc())
            .limit(limit)
            .all()
        )

    def count_all(self) -> int:
        return self.db.query(Alert).count()
    
    def count_by_status(self, status: AlertStatus) -> int:
        return self.db.query(Alert).filter(Alert.status == status).count()

    def count_by_severity(self, severity: Severity) -> int:
        return self.db.query(Alert).filter(Alert.severity == severity).count()

    def save(self, alert: Alert) -> Alert:
        self.db.commit()
        self.db.refresh(alert)
        return alert    
