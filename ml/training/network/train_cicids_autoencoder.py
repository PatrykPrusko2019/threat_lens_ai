from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

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


def prepare_data(df: pd.DataFrame):
    df = df.copy()
    df.columns = df.columns.str.strip()

    if "Label" not in df.columns:
        raise ValueError("Dataset must contain Label column ")
    
    df = df.replace([float("inf"), float("-inf")], pd.NA)
    df = df.dropna()

    y = df["Label"].apply(lambda value: 0 if str(value).upper() in ["BENIGN", "NORMAL", "0"] else 1)

    X = df.drop(columns=["Label"], errors="ignore")
    X = X.drop(columns=["ClassLabel"], errors="ignore")

    X = X.select_dtypes(include=["number"])

    return X, y

def build_autoencoder(input_dim: int) -> tf.keras.Model:
    input_layer = tf.keras.layers.Input(shape=(input_dim,))

    encoded = tf.keras.layers.Dense(64, activation="relu")(input_layer)
    encoded = tf.keras.layers.Dense(32, activation="relu")(encoded)
    encoded = tf.keras.layers.Dense(16, activation="relu")(encoded)

    decoded = tf.keras.layers.Dense(32, activation="relu")(encoded)
    decoded = tf.keras.layers.Dense(64, activation="relu")(decoded)
    decoded = tf.keras.layers.Dense(input_dim, activation="linear")(decoded)

    model = tf.keras.Model(inputs=input_layer, outputs=decoded)

    model.compile(
        optimizer="adam",
        loss="mse",
    )

    return model


def reconstruction_error(model: tf.keras.Model, X: np.ndarray) -> np.ndarray:
    X_pred = model.predict(X, verbose=0)
    errors = np.mean(np.square(X - X_pred), axis=1)
    return errors


def main():
    df = load_dataset()

    print("Dataset shape:", df.shape)

    # if len(df) > 1_000_000:
    #     df = df.sample(n=1_000_000, random_state=42)

    X, y = prepare_data(df)

    print("Features shape:", X.shape)
    print("Labels distribution:")
    print(y.value_counts())

    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X, y, test_size=0.2,
        random_state=42,
        stratify=y,
    )

    # autoencoder is trained only on normal traffic
    X_train_normal = X_train_raw[y_train == 0]

    scaler = StandardScaler()
    X_train_normal_scaled = scaler.fit_transform(X_train_normal)
    X_test_scaled = scaler.transform(X_test_raw)

    model = build_autoencoder(input_dim=X_train_normal_scaled.shape[1])

    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=True
    )

    model.fit(
        X_train_normal_scaled,
        X_train_normal_scaled,
        epochs=20,
        batch_size=256,
        validation_split=0.2,
        callbacks=[early_stopping],
        verbose=1,
    )

    train_errors = reconstruction_error(model, X_train_normal_scaled)
    threshold = float(np.percentile(train_errors, 95))

    test_errors = reconstruction_error(model, X_test_scaled)
    y_pred = (test_errors > threshold).astype(int)

    report = classification_report(y_test, y_pred, zero_division=0)

    print("Threshold:", threshold)
    print(report)

    model_path = MODEL_DIR / "cicids_autoencoder.keras"
    scaler_path = MODEL_DIR / "cicids_autoencoder_scaler.pkl"
    threshold_path = MODEL_DIR / "cicids_autoencoder_threshold.pkl"
    report_path = REPORT_DIR / "cicids_autoencoder_metrics.md"

    model.save(model_path)
    joblib.dump(scaler, scaler_path)
    joblib.dump(threshold, threshold_path)

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("# CICIDS Autoencoder Anomaly Detection Metrics\n\n")
        file.write("## Threshold\n\n")
        file.write(f"`{threshold}`\n\n")
        file.write("## Classification Report\n\n")
        file.write("```text\n")
        file.write(report)
        file.write("\n```")

    print(f"Model saved: {model_path}")
    print(f"Scaler saved: {scaler_path}")    
    print(f"Threshold saved: {threshold_path}")
    print(f"Report saved: {report_path}")

if __name__ == "__main__":
    main()