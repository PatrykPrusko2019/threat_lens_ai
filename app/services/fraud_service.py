from app.db.models.event import SecurityEvent
from app.repositories.event_repository import EventRepository
from app.repositories.alert_repository import AlertRepository
from app.db.models.alert import Alert
from ml.inference.fraud_model import FraudModel

class FraudService:
    def __init__(self, event_repo: EventRepository, alert_repo: AlertRepository):
        self.event_repo = event_repo
        self.alert_repo = alert_repo
        self.model = FraudModel()

    def check_transaction(self, features: list[float]):
        X = [features]

        prediction = self.model.predict(X)[0]
        score = self.model.score(X)[0]

        is_fraud = prediction == -1

        if is_fraud:
            event = SecurityEvent(
                event_repo="fraud_detected",
                severity="high",
                description=f"Fraud detected with score {float(score)}",
            )
            event = self.event_repo.create(event)

            self.alert_repo.create(
                alert=self._build_alert(event.id, score)
            )

        return {
            "fraud": bool(is_fraud),
            "score": float(score),
        }    

    def _build_alert(self, event_id: int, score: float):
        return Alert(
            event_id=event_id,
            title="Fraud detected",
            severity="high",
            risk_score=95,
            description=f"Model flagged fraud with score {float(score)}"
        )