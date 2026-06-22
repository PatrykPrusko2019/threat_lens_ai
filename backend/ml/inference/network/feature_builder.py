from app.schemas.network_event import NetworkEventRequest
from ml.inference.network.cicids_features import CICIDS_FEATURES

class NetworkFeatureBuilder:
    def build(
            self,
            event: NetworkEventRequest,
    ) -> dict[str, float]:
        
        total_packets = event.packets_sent + event.packets_received
        total_bytes = event.bytes_sent + event.bytes_received

        flow_bytes_per_sec = (
            total_bytes / event.duration
            if event.duration > 0
            else 0
        )

        flow_packets_per_sec = (
            total_packets / event.duration
            if event.duration > 0
            else 0
        )

        features = {
            "Flow Duration": event.duration,
            "Total Fwd Packets": event.packets_sent,
            "Total Backward Packets": event.packets_received,
            "Fwd Packets Length Total": event.bytes_sent,
            "Bwd Packets Length Total": event.bytes_received,
            "Flow Bytes/s": flow_bytes_per_sec,
            "Flow Packets/s": flow_packets_per_sec,
            "Packet Length Mean": (
                total_bytes / total_packets
                if total_packets > 0
                else 0
            ),
        }

        # Fill missing features with zeros
        for feature in CICIDS_FEATURES:
            if feature not in features:
                features[feature] = 0.0

        return features        