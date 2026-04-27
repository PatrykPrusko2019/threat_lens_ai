from sqlalchemy.orm import Session
from app.db.models.event import SecurityEvent

class EventRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, event: SecurityEvent) -> SecurityEvent:
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def get_all(self):
        return self.db.query(SecurityEvent).all()    