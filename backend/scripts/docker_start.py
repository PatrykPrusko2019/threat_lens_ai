import os
import subprocess
import sys


def run_command(command: list[str]) -> None:
    print(f"Running: {' '.join(command)}")
    subprocess.run(command, check=True)


def main() -> None:
    print("Starting ThreatLens AI backend container...")

    run_command([sys.executable, "scripts/prepare_models.py"])

    run_command(["alembic", "upgrade", "head"])

    run_command([sys.executable, "scripts/create_admin.py"])
    
    run_command([sys.executable, "scripts/seed_demo_data.py"])

    print("Starting FastAPI backend...")

    os.execvp(
        "uvicorn",
        [
            "uvicorn",
            "app.main:app",
            "--host",
            "0.0.0.0",
            "--port",
            "8000",
        ],
    )


if __name__ == "__main__":
    main()