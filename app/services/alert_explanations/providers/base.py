from abc import ABC, abstractmethod

from app.db.models.alert import Alert

class AlertExplanationProvider(ABC):
    @abstractmethod
    def generate(self, alert: Alert) -> dict:
        pass

    