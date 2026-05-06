import joblib
import numpy as np
from ml.inference.network.cicids_features import CICIDS_FEATURES

MODEL_PATH = "ml/models/network/cicids_random_forest_model.pkl"

class CICIDSModel:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

    def predict(self, features: dict[str, float]) -> dict:
        missing_features = [feature for feature in CICIDS_FEATURES if feature not in features]
        
        if missing_features:
            raise ValueError(
                f"Missing required features: {missing_features[:10]}"
            )

        ordered_features = [features[feature] for feature in CICIDS_FEATURES]

        X = np.array(ordered_features).reshape(1, -1)

        prediction = int(self.model.predict(X)[0])
        probability = self.model.predict_proba(X)[0]
        attack_probability = float(probability[1])

        return {
            "intrusion": bool(prediction),
            "attack_probability": attack_probability
        }    