from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

DATA_FILE = Path("ml/data/cicids/cic-collection.parquet")
MODEL_DIR = Path("ml/models/network")
REPORT_DIR = Path("ml/reports")

MODEL_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def load_dataset() -> pd.DataFrame:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")
    
    print(f"Loading dataset: {DATA_FILE}")
    return pd.read_parquet(DATA_FILE)

def find_label_column(df: pd.DataFrame) -> str:
    columns = ["Label", "label", "Attack", "attack", "Class", "class"]

    for column in columns:
        if column in df.columns:
            return column
        
    raise ValueError(f"Label column not found. Available columns: {df.columns.tolist()}")    

def prepare_data(df: pd.DataFrame):
    df = df.copy()
    df.columns = df.columns.str.strip()

    label_column = find_label_column(df)

    df = df.replace([float("inf"), float("-inf")], pd.NA)
    df = df.dropna()

    y = df[label_column].apply( lambda value: 0 if str(value).upper() in ["BENIGN", "NORMAL", "0"] else 1 )

    X = df.drop(columns=[label_column])

    for column in X.select_dtypes(include=["object"]).columns:
        encoder = LabelEncoder()
        X[column] = encoder.fit_transform(X[column].astype(str))

    X = X.select_dtypes(include=["number"])

    if X.empty:
        raise ValueError("No numeric features found after preprocessing") 

    return X, y  

def train_model(X_train):
    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,
        random_state=42,
        n_jobs=-1,
    ) 
    model.fit(X_train)
    return model

def evaluate_model(model, X_test, y_test) -> str:
    predictions = model.predict(X_test)

    y_pred = [1 if pred == -1 else 0 for pred in predictions]

    return classification_report(y_test, y_pred)

def save_report(report: str) -> None:
    report_path = REPORT_DIR / "cicids_metrics.md"

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("# CICIDS Intrusion Detection Metrics\n\n")
        file.write("```text\n")
        file.write(report)
        file.write("\n```")

        print(f"Report saved: {report_path}")


def save_model(model) -> None:
    model_path = MODEL_DIR / "cicids_intrusion_model.pkl"
    joblib.dump(model, model_path)
    print(f"Model saved: {model_path}")        


def main():
    df = load_dataset()

    print("Dataset shape:", df.shape)
    print("Columns:", df.columns.tolist())

    # if len(df) > 100_000:
    #     df = df.sample(n=100_000, random_state=42)

    X, y = prepare_data(df)

    print("Features shape:", X.shape)
    print("Labels distribution")
    print(y.value_counts())

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = train_model(X_train)

    report = evaluate_model(model, X_test, y_test)

    print(report)

    save_model(model)
    save_report(report)

if __name__ == "__main__":
    main()    
