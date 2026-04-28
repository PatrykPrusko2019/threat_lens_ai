from sqlalchemy.orm import Session

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
    

    def save(self, alert: Alert) -> Alert:
        self.db.commit()
        self.db.refresh(alert)
        return alert    
