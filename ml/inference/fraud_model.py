import joblib

class FraudModel:
    def __init__(self):
        self.model = joblib.load("ml/models/fraud_model.pkl")

    def predict(self, X):
                return self.model.predict(X)

    def score(self, X):
           return self.model.decision_function(X)    