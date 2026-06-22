import pandas as pd
from sklearn.metrics import classification_report
import joblib

df = pd.read_csv("ml/data/creditcard.csv")

y_true = df["Class"]
X = df.drop(columns=["Class"])
model = joblib.load("ml/models/fraud_model.pkl")
y_pred = model.predict(X)

# IsolationForest:
# -1 = anomaly (fraud)
# 1 = normal

y_pred = [1 if p == -1 else 0 for p in y_pred]
print(classification_report(y_true, y_pred))

