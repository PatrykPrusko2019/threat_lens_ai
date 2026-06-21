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

    def get_all(
        self,
        event_type: str | None = None,
        severity: str | None = None,
        source_ip: str | None = None,
        limit: int = 50,
    ) -> list[SecurityEvent]:
        query = self.db.query(SecurityEvent)

        if event_type:
            query = query.filter(SecurityEvent.event_type == event_type)

        if severity:
            query = query.filter(SecurityEvent.severity == severity)

        if source_ip:
            query = query.filter(SecurityEvent.source_ip == source_ip)

        return (
            query
            .order_by(SecurityEvent.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_by_id(self, event_id: int) -> SecurityEvent | None:
        return (
            self.db.query(SecurityEvent)
            .filter(SecurityEvent.id == event_id)
            .first()
        )            
            