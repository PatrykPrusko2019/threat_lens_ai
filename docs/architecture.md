# ThreatLens AI — Architecture

## Overview

ThreatLens AI is an AI-powered cybersecurity platform for:

- Fraud detection
- Intrusion detection
- Anomaly detection
- Alert management

The system combines:

- Machine learning
- Deep learning
- Rule-based cybersecurity detection

---

## High-Level Architecture

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
Detection
  ↓
Security Event
  ↓
Alert