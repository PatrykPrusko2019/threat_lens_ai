from app.db.models.alert import Alert
from app.db.models.event import SecurityEvent
from app.repositories.alert_repository import AlertRepository
from app.repositories.event_repository import EventRepository
from ml.inference.network.cicids_model import CICIDSModel


class IntrusionService:
    def __init__(self, event_repo: EventRepository, alert_repo: AlertRepository) -> None:
        self.event_repo = event_repo
        self.alert_repo = alert_repo
        self.model = CICIDSModel()


    def check_intrusion(self, features: dict[str, float]) -> dict:
        result = self.model.predict(features)

        if not result["intrusion"]:
            return {
                "intrusion": False,
                "attack_probability": result["attack_probability"],
                "event_id": None,
                "alert_id": None
            }

        event = SecurityEvent(
            event_type="network_intrusion_detected",
            severity="critical",
            source_ip=None,
            description=(
                "Network intrusion detected by CICIDS RandomForest model. "
                f"Attack probability: {result['attack_probability']:.4f}"
            )
        )

        event = self.event_repo.create(event)

        alert = Alert(
            event_id=event.id,
            title="Network intrusion detected",
            severity="critical",
            risk_score=95,
            description=(
                "CICIDS model classified network traffic as malicious. "
                f"Attack probability: {result['attack_probability']:.4f}"
            )
        )

        alert = self.alert_repo.create(alert)

        return {
            "intrusion": True,
            "attack_probability": result["attack_probability"],
            "event_id": event.id,
            "alert_id": alert.id
        }    
        