from pathlib import Path
from zipfile import ZipFile


MODEL_ARCHIVES_DIR = Path("ml/model_archives")
MODELS_DIR = Path("ml/models")

REQUIRED_MODEL_FILES = [
    MODELS_DIR / "fraud_model.pkl",
    MODELS_DIR / "network" / "cicids_random_forest_model.pkl",
    MODELS_DIR / "network" / "cicids_autoencoder.keras",
    MODELS_DIR / "network" / "cicids_autoencoder_scaler.pkl",
    MODELS_DIR / "network" / "cicids_autoencoder_threshold.pkl",
]


def models_are_ready() -> bool:
    return all(model_path.exists() for model_path in REQUIRED_MODEL_FILES)


def print_missing_models() -> None:
    missing_models = [
        model_path for model_path in REQUIRED_MODEL_FILES if not model_path.exists()
    ]

    if not missing_models:
        return

    print("Missing ML model files:")

    for model_path in missing_models:
        print(f"- {model_path}")


def unpack_model_archives() -> None:
    archives = sorted(MODEL_ARCHIVES_DIR.glob("*.zip"))

    if not archives:
        raise RuntimeError(
            "ML models are missing and no ZIP archives were found in ml/model_archives."
        )

    for archive_path in archives:
        print(f"Unpacking model archive: {archive_path}")

        with ZipFile(archive_path, "r") as archive:
            archive.extractall(MODELS_DIR)

        print(f"Archive unpacked successfully: {archive_path}")

    print("ZIP archives were left unchanged.")


def main() -> None:
    print("Preparing ML model artifacts...")

    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    if models_are_ready():
        print("ML models already exist. Skipping archive unpacking.")
        return

    print_missing_models()

    if not MODEL_ARCHIVES_DIR.exists():
        raise RuntimeError(
            "ML models are missing and ml/model_archives directory does not exist."
        )

    unpack_model_archives()

    if models_are_ready():
        print("ML model artifacts prepared successfully.")
        return

    print_missing_models()

    raise RuntimeError(
        "Model archive was unpacked, but required ML model files are still missing."
    )


if __name__ == "__main__":
    main()