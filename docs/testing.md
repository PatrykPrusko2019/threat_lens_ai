# Testing

This document describes the current testing strategy used in **ThreatLens AI**.

The project uses **pytest** together with FastAPI **TestClient** to verify API availability, authentication protection, and basic security behavior of core endpoints.

---

## Test Stack

The current test setup uses:

- `pytest` — Python testing framework
- `FastAPI TestClient` — testing FastAPI endpoints without running Uvicorn manually
- `httpx` — HTTP client used internally by TestClient
- `pytest-cov` — planned for test coverage reporting

---

## Test Structure

Tests are organized under the main `tests/` directory:

```text
tests/
├── conftest.py
├── integration/
│   ├── test_health.py
│   └── test_auth_protection.py
├── unit/
└── e2e/
```

### `tests/conftest.py`

Defines reusable test fixtures, including the FastAPI `TestClient`.

### `tests/integration/test_health.py`

Verifies that the application exposes basic operational endpoints.

### `tests/integration/test_auth_protection.py`

Verifies that protected API endpoints cannot be accessed without authentication.

---

## What Is Tested Currently

### Health and Root Endpoints

The following endpoints are tested:

```http
GET /health
GET /
```

These tests verify that the application is available and returns expected basic responses.

---

## Authentication Protection

The following protected endpoints are tested without JWT authentication:

```http
GET /users/me
GET /users/
GET /alerts/
POST /intrusion/check
POST /autoencoder/check
```

Expected result:

```text
401 Unauthorized
or
403 Forbidden
```

This confirms that unauthenticated users cannot access protected API resources.

---

## Test Results

Current test result:

```text
7 passed
```

Screenshot from local test execution:

![Core API Tests](images/pytest_core_api_tests.PNG)

---

## Why These Tests Matter

ThreatLens AI processes cybersecurity events, intrusion detection results, anomaly detection responses, and security alerts.

Because of that, API protection is a critical part of the system.

These tests verify that:

- protected endpoints require authentication
- security-sensitive endpoints are not publicly accessible
- the application starts correctly
- the basic API contract remains stable

---

## Current Test Coverage

Current test coverage focuses on:

| Area | Status |
|---|---|
| Health endpoints | Implemented |
| Root endpoint | Implemented |
| Protected users endpoints | Implemented |
| Protected alerts endpoint | Implemented |
| Protected intrusion endpoint | Implemented |
| Protected autoencoder endpoint | Implemented |
| Login / JWT tests | Planned |
| Admin vs user permission tests | Planned |
| Alert lifecycle tests | Planned |
| ML response contract tests | Planned |

---

## Future Test Improvements

Planned future tests include:

- user registration tests
- login and JWT token validation
- admin vs regular user authorization
- alert lifecycle tests
- intrusion detection response validation
- autoencoder response validation
- invalid input validation tests
- database integration tests
- CI test execution with GitHub Actions
- test coverage reports

---

## Running Tests

Run all tests:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

Run tests with coverage:

```bash
pytest --cov=app
```