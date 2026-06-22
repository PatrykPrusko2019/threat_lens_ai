from app.db.models.alert import Alert
from app.db.models.event import SecurityEvent
from app.repositories.alert_repository import AlertRepository
from app.repositories.event_repository import EventRepository
from app.schemas.network_event import NetworkEventRequest
from app.services.intrusion_rules import IntrusionRuleEngine
from ml.inference.network.cicids_model import CICIDSModel
from ml.inference.network.feature_builder import NetworkFeatureBuilder


class IntrusionService:
    def __init__(self, event_repo: EventRepository, alert_repo: AlertRepository) -> None:
        self.event_repo = event_repo
        self.alert_repo = alert_repo
        self.rule_engine = IntrusionRuleEngine()
        self.model = CICIDSModel()
        self.feature_builder = NetworkFeatureBuilder()

    def check_intrusion(self, event: NetworkEventRequest) -> dict:
        features = self.feature_builder.build(event)

        rule_triggered, rule_reason = self.rule_engine.evaluate(event)
        model_result = self.model.predict(features)

        intrusion_detected = model_result["intrusion"] or rule_triggered

        if not intrusion_detected:
            return {
                "intrusion": False,
                "attack_probability": model_result["attack_probability"],
                "detection_source": None,
                "detection_reason": None,
                "event_id": None,
                "alert_id": None,
            }

        detection_source = "rule_engine" if rule_triggered else "ai_model"
        detection_reason = rule_reason if rule_reason else "AI model classified traffic as malicious"

        event_description = (
            "Suspicious network activity detected by intrusion detection pipeline. "
            f"Detection source: {detection_source}. "
            f"Reason: {detection_reason}. "
            f"AI attack probability: {model_result['attack_probability']:.4f}."
        )

        alert_description = (
            "Potential network intrusion detected. "
            f"Detection source: {detection_source}. "
            f"Reason: {detection_reason}. "
            f"Attack probability: {model_result['attack_probability']:.4f}. "
            "Immediate investigation recommended."
        )

        event_record = SecurityEvent(
            event_type="network_intrusion_detected",
            severity="critical",
            source_ip=event.source_ip,
            description=event_description,
        )

        event_record = self.event_repo.create(event_record)

        alert = Alert(
            event_id=event_record.id,
            title="Network intrusion detected",
            severity="critical",
            risk_score=95,
            description=alert_description,
        )

        alert = self.alert_repo.create(alert)

        return {
            "intrusion": True,
            "attack_probability": model_result["attack_probability"],
            "detection_source": detection_source,
            "detection_reason": detection_reason,
            "event_id": event_record.id,
            "alert_id": alert.id,
            "description": alert_description
        }