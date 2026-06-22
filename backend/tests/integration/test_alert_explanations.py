from app.db.enums import AlertStatus, Severity
from app.db.models.alert import Alert
from app.db.models.event import SecurityEvent
from app.db.models.user import User


def register_user(client, email: str, password: str = "Password123!") -> None:
    payload = {
        "email": email,
        "password": password,
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 201


def login_user(client, email: str, password: str = "Password123!") -> str:
    payload = {
        "email": email,
        "password": password,
    }

    response = client.post("/auth/login", json=payload)

    assert response.status_code == 200

    return response.json()["access_token"]


def create_user_token(client, email: str, password: str = "Password123!") -> str:
    register_user(client, email, password)

    return login_user(client, email, password)


def make_user_admin(db_session, email: str) -> None:
    user = db_session.query(User).filter(User.email == email).first()

    assert user is not None

    user.role = "admin"
    db_session.commit()


def create_admin_token(
    client,
    db_session,
    email: str,
    password: str = "Password123!",
) -> str:
    register_user(client, email, password)
    make_user_admin(db_session, email)

    return login_user(client, email, password)


def create_security_event(db_session) -> SecurityEvent:
    event = SecurityEvent(
        event_type="failed_transaction",
        severity="high",
        source_ip="192.168.1.10",
        description="AI model detected suspicious transaction behavior.",
    )

    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)

    return event


def create_alert(db_session, event_id: int) -> Alert:
    alert = Alert(
        event_id=event_id,
        title="Anomaly detected: failed_transaction",
        severity=Severity.HIGH,
        status=AlertStatus.OPEN,
        risk_score=90,
        description="AI model detected suspicious event with high risk score.",
    )

    db_session.add(alert)
    db_session.commit()
    db_session.refresh(alert)

    return alert


def test_admin_can_explain_alert(client, db_session):
    token = create_admin_token(
        client,
        db_session,
        "alert-explanation-admin@example.com",
    )

    event = create_security_event(db_session)
    alert = create_alert(db_session, event.id)

    response = client.post(
        f"/alerts/{alert.id}/explain",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["alert_id"] == alert.id
    assert data["title"] == alert.title
    assert data["severity"] == Severity.HIGH.value
    assert data["risk_score"] == 90
    assert data["status"] == AlertStatus.OPEN.value
    assert data["source"] == "rule_based"

    assert "summary" in data
    assert "severity_explanation" in data
    assert "possible_causes" in data
    assert "recommended_actions" in data

    assert isinstance(data["possible_causes"], list)
    assert isinstance(data["recommended_actions"], list)
    assert len(data["possible_causes"]) > 0
    assert len(data["recommended_actions"]) > 0


def test_alert_explanation_contains_transaction_causes(client, db_session):
    token = create_admin_token(
        client,
        db_session,
        "transaction-explanation-admin@example.com",
    )

    event = create_security_event(db_session)
    alert = create_alert(db_session, event.id)

    response = client.post(
        f"/alerts/{alert.id}/explain",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert "Suspicious transaction behavior." in data["possible_causes"]
    assert data["severity_explanation"].startswith("High severity")


def test_regular_user_cannot_explain_alert(client, db_session):
    token = create_user_token(
        client,
        "regular-explanation-user@example.com",
    )

    event = create_security_event(db_session)
    alert = create_alert(db_session, event.id)

    response = client.post(
        f"/alerts/{alert.id}/explain",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403


def test_explain_non_existing_alert_returns_404(client, db_session):
    token = create_admin_token(
        client,
        db_session,
        "missing-alert-explanation-admin@example.com",
    )

    response = client.post(
        "/alerts/999999/explain",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Alert not found"