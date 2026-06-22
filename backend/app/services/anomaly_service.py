from app.db.models.alert import Alert
from app.repositories.alert_repository import AlertRepository
from app.repositories.event_repository import EventRepository
from ml.inference.anomaly import AnomalyDetector
from ml.inference.features import event_to_features

class AnomalyService:
    def __init__(self, event_repo: EventRepository, alert_repo: AlertRepository):
        self.event_repo = event_repo
        self.alert_repo = alert_repo
        self.detector = AnomalyDetector()

    def analyze(self):
        events = self.event_repo.get_all()

        if not events:
            return []
        
        X = [event_to_features(e) for e in events]

        self.detector.fit(X)

        predictions = self.detector.predict(X)
        scores = self.detector.score(X)

        result = []

        for e, pred, score in zip(events, predictions, scores):
            is_anomaly = bool(pred == -1)
            risk_score = self._calculate_risk_score(is_anomaly, e.severity)

            if is_anomaly:
                alert = Alert(
                    event_id=e.id,
                    title=f"Anomaly detected: {e.event_type}",
                    severity=e.severity,
                    risk_score=risk_score,
                    description=f"AI model detected suspicious event with score {float(score)}",
                )
                self.alert_repo.create(alert)
                
            
            result.append({
                "event_id": int(e.id),
                "event_type": e.event_type,
                "anomaly": is_anomaly,
                "score": float(score),
                "risk_score": risk_score,
            })

        return result
    

    def _calculate_risk_score(self, is_anomaly: bool, severity: str) -> int:
        score = 0

        if is_anomaly:
            score += 60

        severity = severity.lower()

        if severity == "low":
            score += 10
        elif severity == "medium":
            score += 20
        elif severity == "high":
            score += 30
        elif severity == "critical":
            score += 40

        return min(score, 100)
    
                    

        

