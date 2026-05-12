from app.db.models.alert import Alert
from app.db.models.event import SecurityEvent
from app.repositories.alert_repository import AlertRepository
from app.repositories.event_repository import EventRepository
from app.schemas.network_event import NetworkEventRequest
from ml.inference.network.autoencoder_model import CICIDSAutoencoderModel
from ml.inference.network.feature_builder import NetworkFeatureBuilder

class AutoencoderService:
    def __init__(
            self,
            event_repo: EventRepository,
            alert_repo: AlertRepository,
    ) -> None:
        self.event_repo = event_repo
        self.alert_repo = alert_repo
        self.model = CICIDSAutoencoderModel()
        self.feature_builder = NetworkFeatureBuilder()

    def check_anomaly(self, event: NetworkEventRequest) -> dict:
        features = self.feature_builder.build(event)
        result = self.model.predict(features)

        if not result["anomaly"]:
            return {
                **result,
                "event_id": None,
                "alert_id": None,
            }
        
        event_description = (
            "Network anomaly detected by TensorFlow/Keras Autoencoder. "
            f"Anomaly score: {result['anomaly_score']:.2f}. "
            f"Raw anomaly score: {result['raw_anomaly_score']:.4f}. "
            f"Reconstructuin error: {result['reconstruction_error']:.6f}. "
            f"Threshold: {result['threshold']:.6f}."
        )

        alert_description = (
            "Potential anomalous network behavior detected by Autoencoder model. "
            f"Normalized anomaly score: {result['anomaly_score']:.2f}/100. "
            "Security investigation recommended."
        )

        event_record = SecurityEvent(
            event_type="autoencoder_network_anomaly",
            severity=self._map_severity(result["anomaly_score"]),
            source_ip=event.source_ip,
            description=event_description,
        )

        event_record = self.event_repo.create(event_record)

        alert = Alert(
            event_id=event_record.id,
            title="Autoencoder network anomaly detected",
            severity=self._map_severity(result["anomaly_score"]),
            risk_score=self._map_risk_score(result["anomaly_score"]),
            description=alert_description,
        )

        alert = self.alert_repo.create(alert)

        return {
            **result,
            "event_id": event_record.id,
            "alert_id": alert.id,
        }
    


    def _map_risk_score(self, anomaly_score: float) -> int:
        return min(max(int(anomaly_score), 1), 100)
    

    def _map_severity(self, anomaly_score: float) -> str:
        if anomaly_score >= 70:
            return "critical"
        
        if anomaly_score >= 40:
            return "high"
        
        if anomaly_score >= 15:
            return "medium"
        
        return "low"