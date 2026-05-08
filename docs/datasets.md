# Datasets

This document describes datasets used in ThreatLens AI for:

- Network intrusion detection
- Fraud detection
- Deep learning anomaly detection
- Cybersecurity experiments

---

# CICIDS Collection

## Purpose

Dataset used for:

- Network intrusion detection
- Autoencoder anomaly detection
- Network traffic classification
- Security event analysis

---

## Source

https://www.kaggle.com/datasets/dhoogla/cicidscollection

---

## Local Path

```text
ml/data/cicids/cic-collection.parquet
```

---

## Description

The CICIDS dataset contains realistic network traffic data with:

- Normal traffic
- DDoS attacks
- Port scans
- Brute force attacks
- Botnet activity
- Web attacks
- Other malicious traffic patterns

The dataset is used for:

- RandomForest intrusion detection
- IsolationForest anomaly detection
- TensorFlow/Keras Autoencoder experiments

---

## Features

Main feature categories:

- Packet statistics
- Flow duration
- Traffic rates
- Packet sizes
- Timing statistics
- Header information

---

## Labels

```text
0 → normal traffic
1 → malicious traffic
```

---

# Credit Card Fraud Dataset

## Purpose

Dataset used for:

- Fraud detection
- Financial anomaly detection
- Transaction risk analysis
- AI-based fraud classification

---

## Source

https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

---

## Local Path

```text
ml/data/fraud/creditcard.csv
```

---

## Description

The dataset contains anonymized credit card transactions.

It includes:

- Normal financial transactions
- Fraudulent transactions

The dataset is highly imbalanced and is useful for:

- Fraud detection experiments
- Anomaly detection research
- Autoencoder fraud analysis
- Binary classification tasks

---

## Features

The dataset contains:

- PCA-transformed features (`V1–V28`)
- Transaction amount
- Transaction time
- Fraud label

---

## Labels

```text
0 → legitimate transaction
1 → fraudulent transaction
```

---

# Notes

Datasets are NOT included in this repository because of GitHub file size limitations.

Download datasets manually and place them in the specified local directories.

---

# Future Dataset Plans

Planned future datasets:

- UNSW-NB15
- NSL-KDD
- Darknet traffic datasets
- Malware behavior datasets
- Threat intelligence feeds
- SIEM / SOC log datasets