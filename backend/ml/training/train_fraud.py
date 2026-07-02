import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib


def main():
    df = pd.read_csv("ml/data/creditcard.csv")

    X = df.drop(columns=["Class"])
    model = IsolationForest(contamination=0.001, random_state=42)
    model.fit(X)

    joblib.dump(model, "ml/models/fraud_model.pkl")
    print("saved model")

if __name__ == "__main__":
    main()

