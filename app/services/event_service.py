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
    
    def get_events(self):
        return self.repo.get_all()
    
    