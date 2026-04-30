import joblib
import numpy as np

MODEL_PATH = "ml/models/network/cicids_random_forest_model.pkl"
EXPECTED_FEATURES = 57

class CICIDSModel:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

    def predict(self, features: list[float]):
        if len(features) != EXPECTED_FEATURES:
            raise ValueError(
                f"Invalid number of features. Expected {EXPECTED_FEATURES}, got {len(features)}."
            )

        X = np.array(features).reshape(1, -1)
        prediction = self.model.predict(X)[0]

        probability = self.model.predict_proba(X)[0]
        attack_probability = float(probability[1])

        return {
            "intrusion": bool(prediction),
            "attack_probability": attack_probability
        }    