from app.db.models.event import SecurityEvent
from app.repositories.event_repository import EventRepository


class EventService:
    def __init__(self, repo: EventRepository):
        self.repo = repo

    def create_event(self, data, user_id: int | None):
        event = SecurityEvent(
            event_type=data.event_type,
            severity=data.severity,
            source_ip=data.source_ip,
            description=data.description,
            user_id=user_id,
        )    
        return self.repo.create(event)
    
    def get_events(
            self,
            event_type: str | None = None,
            severity: str | None = None,
            source_ip: str | None = None,
            limit: int = 50,
    ):
        return self.repo.get_all(
            event_type=event_type,
            severity=severity,
            source_ip=source_ip,
            limit=limit,
        )
    
    def get_event_by_id(self, event_id: int):
        event = self.repo.get_by_id(event_id)

        if not event:
            raise ValueError("Event not found")
        
        return event