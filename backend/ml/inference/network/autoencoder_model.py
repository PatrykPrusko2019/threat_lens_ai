from pathlib import Path
import joblib
import numpy as np
import tensorflow as tf
import math

from ml.inference.network.cicids_features import CICIDS_FEATURES

MODEL_PATH = Path("ml/models/network/cicids_autoencoder.keras")
SCALER_PATH = Path("ml/models/network/cicids_autoencoder_scaler.pkl")
THRESHOLD_PATH = Path("ml/models/network/cicids_autoencoder_threshold.pkl")

class CICIDSAutoencoderModel:
    def __init__(self):
        self.model = tf.keras.models.load_model(MODEL_PATH)

        self.scaler = joblib.load(SCALER_PATH)

        self.threshold = joblib.load(THRESHOLD_PATH)

    def predict(
            self,
            features: dict[str, float],
    ) -> dict:
           
           missing_features = [
                feature
                for feature in CICIDS_FEATURES
                if feature not in features
           ]

           if missing_features:
                raise ValueError(
                     f"Missing required features: {missing_features[:10]}"
                )
           
           ordered_features = [
                features[feature]
                for feature in CICIDS_FEATURES
           ]

           X = np.array(ordered_features).reshape(1, -1)

           X_scaled = self.scaler.transform(X)

           X_pred = self.model.predict(X_scaled, verbose=0)

           reconstruction_error = float(
                np.mean(np.square(X_scaled - X_pred))
           )

           anomaly = reconstruction_error > self.threshold

           raw_anomaly_score = reconstruction_error / self.threshold 

           anomaly_score = min(
                math.log1p(raw_anomaly_score) * 10,
                100.0,
           )

           return {
                "anomaly": bool(anomaly),
                "anomaly_score": float(anomaly_score),
                "raw_anomaly_score": float(raw_anomaly_score),
                "reconstruction_error": reconstruction_error,
                "threshold": float(self.threshold),
           }
