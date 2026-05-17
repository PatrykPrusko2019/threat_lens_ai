from app.db.enums import AlertStatus, Severity
from app.db.models.alert import Alert
from app.db.models.event import SecurityEvent
from app.db.models.user import User

def create_user(client, email: str, password: str = "Password123!") -> str:
    payload = {
        "email": email,
        "password": password,
    }

    client.post("/auth/register", json=payload)

    login_response = client.post("/auth/login", json=payload)

    assert login_response.status_code == 200

    return login_response.json()["access_token"]

def make_user_admin(db_session, email: str) -> None:
    user = db_session.query(User).filter(User.email == email).first()

    assert user is not None

    user.role = "admin"
    db_session.commit()

def create_security_event(db_session) -> SecurityEvent:
        event = SecurityEvent(
             event_type="test_security_event",
             severity="medium",
             source_ip="192.168.1.10",
             description="Test security event for alert lifecycle tests.",
        )

        db_session.add(event)
        db_session.commit()
        db_session.refresh(event)

        return event

def create_alert(db_session, event_id: int) -> Alert:
     alert = Alert(
          event_id=event_id,
          title="Test alert",
          severity=Severity.MEDIUM,
          status=AlertStatus.OPEN,
          risk_score=50,
          description="Test alert for lifecycle tests.",
     )

     db_session.add(alert)
     db_session.commit()
     db_session.refresh(alert)

     return alert

def test_admin_can_list_alerts(client, db_session):
     admin_email = "alerts-admin@example.com"
     token = create_user(client, admin_email)
     make_user_admin(db_session, admin_email)

     event = create_security_event(db_session)
     alert = create_alert(db_session, event.id)

     response = client.get(
          "/alerts/",
          headers={"Authorization": f"Bearer {token}"},
     )

     assert response.status_code == 200

     data = response.json()

     assert isinstance(data, list)
     assert len(data) == 1
     assert data[0]["id"] == alert.id
     assert data[0]["title"] == "Test alert"
     assert data[0]["status"] == AlertStatus.OPEN.value
     assert data[0]["severity"] == Severity.MEDIUM.value
     assert data[0]["risk_score"] == 50

def test_regular_user_cannot_list_alerts(client, db_session):
     token = create_user(client, "regular-alerts-user@example.com")

     event = create_security_event(db_session)
     create_alert(db_session, event.id)

     response = client.get(
          "/alerts/",
          headers={"Authorization": f"Bearer {token}"},
     )

     assert response.status_code == 403

def test_admin_can_close_alert(client, db_session):
     admin_email = "close-alert-admin@example.com"
     token = create_user(client, admin_email)
     make_user_admin(db_session, admin_email)

     event = create_security_event(db_session)
     alert = create_alert(db_session, event.id)

     payload = {
          "status": AlertStatus.CLOSED.value,
     }

     response = client.patch(
          f"/alerts/{alert.id}",
          json=payload,
          headers={"Authorization": f"Bearer {token}"},
     )

     assert response.status_code == 200

     data = response.json()

     assert data["id"] == alert.id
     assert data["status"] == AlertStatus.CLOSED.value
     assert data["event_id"] == event.id

def test_regular_user_cannot_close_alert(client, db_session):
     token = create_user(client, "regular-close-alert@example.com")

     event = create_security_event(db_session)
     alert = create_alert(db_session, event.id)

     payload = {
          "status": AlertStatus.CLOSED.value,
     }

     response = client.patch(
          f"/alerts/{alert.id}",
          json=payload,
          headers={"Authorization": f"Bearer {token}"},
     )

     assert response.status_code == 403

def test_update_non_existing_alert_returns_404(client, db_session):
     admin_email = "missing-alert-admin@example.com"
     token = create_user(client, admin_email)
     make_user_admin(db_session, admin_email)

     payload = {
          "status": AlertStatus.CLOSED.value,
     }

     response = client.patch(
          "/alerts/999999",
          json=payload,
          headers={"Authorization": f"Bearer {token}"},
     )

     assert response.status_code == 404
     assert response.json()["detail"] == "Alert not found"

def test_invalid_alert_status_returns_422(client, db_session):
     admin_email = "invalid-status-admin@example.com"
     token = create_user(client, admin_email)
     make_user_admin(db_session, admin_email)

     event = create_security_event(db_session)
     alert = create_alert(db_session, event.id)

     payload = {
          "status": "invalid_status",
     }

     response = client.patch(
          f"/alerts/{alert.id}",
          json=payload,
          headers={"Authorization": f"Bearer {token}"},
     )

     assert response.status_code == 422              