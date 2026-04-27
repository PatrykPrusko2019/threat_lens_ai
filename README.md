# 🚀 ThreatLens AI — Cybersecurity & Fraud Detection Platform

ThreatLens AI is a backend-driven platform for detecting anomalies, fraud, and security threats using machine learning and rule-based analysis.

The system processes security events, analyzes them using AI models, calculates risk scores, and generates alerts — similar to real-world SIEM (Security Information and Event Management) systems.

---

## 🧠 Key Features

* 🔐 **Authentication & Authorization**

  * JWT-based authentication
  * Role-based access control (user/admin)

* 📊 **Security Events**

  * Logging and storing system events
  * Event classification (severity, type, source)

* 🤖 **Anomaly Detection (AI)**

  * Isolation Forest model for anomaly detection
  * Detection of suspicious behavior in event streams

* 💳 **Fraud Detection (Kaggle Dataset)**

  * Trained on real-world credit card fraud dataset
  * Offline training + API inference
  * Real-time fraud scoring

* ⚠️ **Alert System**

  * Automatic alert generation for anomalies
  * Risk scoring mechanism (0–100)
  * Alert lifecycle (open/closed)

* 🧱 **Clean Architecture**

  * Separation of concerns (API, services, repositories, models)
  * Scalable modular design

---

## 🏗️ Architecture

```
Client → API (FastAPI)
       → Services
       → Repositories
       → Database (PostgreSQL)

AI Pipeline:
Events → Feature Engineering → Model → Risk Score → Alert
```

---

## 🧰 Tech Stack

* **Backend**: FastAPI (Python)
* **Database**: PostgreSQL
* **ORM**: SQLAlchemy
* **Migrations**: Alembic
* **AI/ML**: scikit-learn (Isolation Forest)
* **Containerization**: Docker
* **Authentication**: JWT

---

## 📂 Project Structure

```
app/
  api/
  services/
  repositories/
  db/
  schemas/
ml/
  training/
  inference/
docker/
migrations/
```

---

## 🧪 Machine Learning

The anomaly detection model is trained using:

* Isolation Forest (unsupervised learning)
* Real-world fraud dataset (Kaggle)
* Evaluation using classification metrics (precision, recall, F1-score)

---

## 🚀 How to Run

```bash
docker compose up -d
alembic upgrade head
uvicorn app.main:app --reload
```

---

## 🔍 Example API Endpoints

* `POST /auth/login`
* `GET /users/me`
* `POST /events`
* `GET /anomaly`
* `POST /fraud/check`
* `GET /alerts`

---

## 🎯 Project Goal

This project demonstrates:

* AI integration in backend systems
* Cybersecurity event analysis
* Fraud detection using real datasets
* Scalable backend architecture

---

## 💡 Future Improvements

* Advanced ML models (Autoencoders, LSTM)
* Real-time streaming (Kafka)
* Dashboard (React)
* RAG + LLM-based threat analysis
* Cloud deployment (Azure)
