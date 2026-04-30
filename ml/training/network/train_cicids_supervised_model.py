from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
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
    for column in ["Label", "label", "ClassLabel", "class_label", "Class", "class"]:
        if column in df.columns:
            return column
        
        raise ValueError(f"Label column not found. Columns: {df.columns.tolist()}")
    

def prepare_data(df: pd.DataFrame):
    df = df.copy()
    df.columns = df.columns.str.strip()

    label_column = find_label_column(df)

    df = df.replace([float("inf"), float("-inf")], pd.NA)
    df = df.dropna()

    y = df[label_column].apply( lambda value: 0 if str(value).upper() in ["BENIGN", "NORMAL", "0"] else 1 )
    X = df.drop(columns=[label_column])

    if "CLassLabel" in X.columns:
        X = X.drop(columns=["CLassLabel"])

        for column in X.select_dtypes(include=["object", "string"]).columns:
            encoder = LabelEncoder()
            X[column] = encoder.fit_transform(X[column].astype(str))

    X = X.select_dtypes(include=["number"])

    return X, y

def main():
    df = load_dataset()

    print("Dataset shape:", df.shape)
    print("Columns:", df.columns.tolist())

    # if len(df) > 300_000:
    #     df = df.sample(n=300_000, random_state=42)

    X, y = prepare_data(df)

    print("Features shape:", X.shape)
    print("Labels distribution:")
    print(y.value_counts())

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced"
    )                    

    model. fit(X_train, y_train)
    y_pred = model.predict(X_test)

    report = classification_report(y_test, y_pred)
    matrix = confusion_matrix(y_test, y_pred)

    print(report)
    print("Confusuin matrix:")
    print(matrix)

    model_path = MODEL_DIR / "cicids_random_forest_model.pkl"
    joblib.dump(model, model_path)

    report_path = REPORT_DIR / "cicids_random_forest_metrics.md"
    with open(report_path, "w", encoding="utf-8") as file:
        file.write("# CICIDS Random Forest Intrusion Detection Metrics\n\n")
        file.write("## Classification Report\n\n")
        file.write("```text\n")
        file.write(report)
        file.write("\n```\n\n")
        file.write("## Confusion Matrix\n\n")
        file.write("```text\n")
        file.write(str(matrix))
        file.write("\n```\n")

    print(f"Model saved: {model_path}")
    print(f"Report saved: {report_path}")

if __name__ == "__main__":
    main()        