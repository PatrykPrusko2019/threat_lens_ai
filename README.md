# 🚀 ThreatLens AI

## AI-Powered Cybersecurity & Fraud Detection Platform

ThreatLens AI is an advanced cybersecurity and fraud detection platform built with:

- Machine Learning
- Deep Learning
- Hybrid AI Detection
- Rule-Based Security Analysis

The platform analyzes network traffic and security events, detects anomalies and intrusions, generates alerts, and simulates core SIEM/SOC functionalities used in modern cybersecurity systems.

---

# 🔥 Core Features

## 🔐 Authentication & Authorization

- JWT-based authentication
- Role-based access control (RBAC)
- Admin-protected endpoints
- Secure API access

---

## ⚠️ Intrusion Detection

Hybrid intrusion detection system using:

- RandomForest classifier
- Rule-based cybersecurity engine
- Feature engineering pipeline

Capabilities:

- Network anomaly detection
- Packet flood detection
- Suspicious traffic analysis
- AI-based attack classification
- Automatic `SecurityEvent` creation
- Automatic `Alert` generation

---

## 🧠 Deep Learning Anomaly Detection

ThreatLens AI includes an Autoencoder-based anomaly detection module for identifying suspicious network behavior.

The Autoencoder learns patterns of normal network traffic and detects anomalies using reconstruction error analysis.

Key capabilities:

- Autoencoder-based anomaly detection
- Reconstruction error analysis
- Threshold-based anomaly classification
- Normalized anomaly scoring
- Raw anomaly score for ML/debugging
- Severity mapping based on anomaly score
- Risk score generation
- Automatic `SecurityEvent` creation
- Automatic `Alert` generation
- API-ready response for future dashboards and LLM explanations

---

## 💳 Fraud Detection

Fraud detection module trained on real-world financial transaction datasets:

- Credit card fraud analysis
- Risk scoring
- Suspicious transaction detection
- Machine learning inference

---

## 🚨 Security Events & Alerts

ThreatLens AI generates:

- Security events
- AI-powered alerts
- Risk scores
- Explainable detection details

Alert system features:

- Open/closed lifecycle
- Severity classification
- Event correlation
- Threat tracking

---

# 🏗️ System Architecture

```text
Client
  ↓
FastAPI API
  ↓
Services Layer
  ↓
Repositories Layer
  ↓
PostgreSQL Database

AI Pipeline:
Raw Event
  ↓
Feature Engineering
  ↓
ML / DL Models
  ↓
Detection Engine
  ↓
Security Event
  ↓
Alert
```

---

# 🧰 Tech Stack

## Backend

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic

---

## AI / Machine Learning

- scikit-learn
- TensorFlow
- Keras
- RandomForest
- IsolationForest
- Autoencoder Neural Networks

---

## Security

- JWT Authentication
- RBAC Authorization
- Hybrid AI + Rule Detection

---

## Infrastructure

- Docker
- Docker Compose
- GitHub PR Workflow

---

# 📂 Project Structure

```text
app/
  api/
  services/
  repositories/
  db/
  schemas/

ml/
  training/
  inference/
  models/
  reports/

docs/
  architecture.md
  ml_pipeline.md
  api_examples.md
  datasets.md
  testing.md

docker/
migrations/
tests/
```

---

# 🧪 Machine Learning Pipeline

ThreatLens AI currently supports multiple detection approaches:

| Detection Type | Technology |
|---|---|
| Intrusion Detection | RandomForest |
| Anomaly Detection | IsolationForest |
| Deep Learning Detection | TensorFlow Autoencoder |
| Hybrid Detection | AI + Rule Engine |

---

# 📊 Example API Endpoints

| Endpoint | Description |
|---|---|
| `POST /auth/login` | User authentication |
| `GET /users/me` | Current authenticated user |
| `POST /intrusion/check` | Hybrid network intrusion detection using ML and rule engine |
| `POST /autoencoder/check` | Autoencoder anomaly detection with severity, risk score, event creation, and alert generation |
| `POST /fraud/check` | Fraud detection for financial transactions |
| `GET /alerts` | Generated security alerts |

---

# 📸 API Examples

Detailed API screenshots and examples are available here:

```text
docs/api_examples.md
```

---

# 🧠 Autoencoder Detection Flow

The Autoencoder endpoint provides a complete deep learning anomaly detection flow:

```text
Network Event
  ↓
Feature Engineering
  ↓
Autoencoder Inference
  ↓
Reconstruction Error
  ↓
Anomaly Score
  ↓
Severity + Risk Score
  ↓
SecurityEvent
  ↓
Alert
```

Example Autoencoder response:

```json
{
  "anomaly": true,
  "anomaly_score": 23.59,
  "raw_anomaly_score": 9.58,
  "reconstruction_error": 0.131,
  "threshold": 0.013,
  "severity": "medium",
  "risk_score": 23,
  "event_id": 15,
  "alert_id": 11
}
```

This makes the Autoencoder module ready for future dashboard visualization, alert explanations, and LLM-based security analysis.

---

# 🚀 Running the Project

## Docker

```bash
docker compose up -d
```

---

## Database Migration

```bash
alembic upgrade head
```

---

## Start API

```bash
uvicorn app.main:app --reload
```

---

# 🧪 Testing

ThreatLens AI includes automated backend tests using `pytest` and FastAPI `TestClient`.

The current test suite verifies:

- API health checks
- root endpoint availability
- authentication protection for secured endpoints
- access protection for users, alerts, intrusion detection, and autoencoder endpoints

Run tests:

```bash
pytest -v
```

Current result:

```text
7 passed
```

More details:

```text
docs/testing.md
```

---

# 📚 Datasets

Datasets used in the project:

- CICIDS network intrusion dataset
- Credit card fraud dataset

More information:

```text
docs/datasets.md
```

---

# 📄 Documentation

The project includes continuously updated technical documentation covering:

- System architecture
- AI/ML pipelines
- API examples
- Detection workflows
- Dataset descriptions
- Testing strategy
- Future development plans

Documentation is maintained in:

```text
docs/
```

Additional project notes, experiments, and research materials are also maintained during development.

---

# 🎯 Project Goals

This project focuses on:

- AI integration in backend systems
- Cybersecurity event analysis
- Fraud detection using real-world datasets
- Deep learning anomaly detection
- Hybrid AI security systems
- Scalable backend architecture

---

# 🔮 Future Development

## AI / ML

- LSTM sequence analysis
- Transformer-based detection
- Explainable AI
- Threat scoring systems

---

## LLM & RAG

- AI security assistant
- Threat explanation generation
- RAG knowledge base
- Threat intelligence integration

---

## Frontend

- React dashboard
- Alert management UI
- Threat monitoring panels

---

## Infrastructure

- Azure deployment
- Kafka streaming
- CI/CD pipelines
- Production Docker setup

---

# 📌 Status

🚧 Active development project

The platform is continuously expanded with new AI detection modules and cybersecurity features.

---

# 👨‍💻 Author

Patryk Prusko

AI • Backend • Cybersecurity • Machine Learning