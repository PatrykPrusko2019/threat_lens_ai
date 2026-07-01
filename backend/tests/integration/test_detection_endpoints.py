from app.db.models.user import User


def create_user(client, email: str, password: str = "Password123!") -> str:
    payload = {
        "email": email,
        "password": password,
    }

    register_response = client.post("/auth/register", json=payload)
    assert register_response.status_code == 201

    login_response = client.post("/auth/login", json=payload)
    assert login_response.status_code == 200

    return login_response.json()["access_token"]

def make_user_admin(db_session, email: str) -> None:
    user = db_session.query(User).filter(User.email == email).first()

    assert user is not None
    
    user.role = "admin"
    db_session.commit()

def create_admin_token(client, db_session, email: str) -> str:
    token = create_user(client, email)
    make_user_admin(db_session, email)

    return token

def valid_network_payload() -> dict:
    return {
        "source_ip": "185.220.101.1",
        "destination_ip": "10.0.0.5",
        "protocol": "TCP",
        "duration": 1,
        "bytes_sent": 60000,
        "bytes_received": 10,
        "packets_sent": 1200,
        "packets_received": 1,
    }

def test_regular_user_can_access_intrusion_check(client):
    token = create_user(client, "regular-intrusion@example.com")

    response = client.post(
        "/intrusion/check",
        json=valid_network_payload(),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert "intrusion" in data
    assert "attack_probability" in data

def test_regular_user_can_access_autoencoder_check(client):
    token = create_user(client, "regular-autoencoder@example.com")

    response = client.post(
        "/autoencoder/check",
        json=valid_network_payload(),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert "anomaly" in data

def test_intrusion_check_invalid_payload_returns_422(client, db_session):
    token = create_admin_token(
        client,
        db_session,
        "admin-invalid-intrusion@example.com",
    )

    invalid_payload = {
        "source_ip": "185.220.101.1",
        "destination_ip": "10.0.0.5",
        "protocol": "TCP",
        "duration": 1,
    }

    response = client.post(
        "/intrusion/check",
        json=invalid_payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422

def test_autoencoder_check_invalid_payload_returns_422(client, db_session):
    token = create_admin_token(
        client,
        db_session,
        "admin-invalid-autoencoder@example.com",
    )

    invalid_payload = {
        "source_ip": "185.220.101.1",
        "destination_ip": "10.0.0.5",
        "protocol": "TCP",
        "duration": 1,
    }

    response = client.post(
        "/autoencoder/check",
        json=invalid_payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422

def test_intrusion_check_returns_expected_response_for_admin(
        client,
        db_session,
        monkeypatch,
): 
        from app.api.v1 import intrusion as intrusion_api

        token = create_admin_token(
            client,
            db_session,
            "admin-intrusion-response@example.com",
        )

        def fake_init(self, event_repo, alert_repo):
            # Skip real service initialization to avoid loading ML models in this test.
            pass

        def fake_check_intrusion(self, payload):
            return {
                "intrusion": True,
                "attack_probability": 0.91,
                "detection_source": "rule_engine",
                "detection_reason": "Possible packet flood attack",
                "event_id": 1,
                "alert_id": 1,
            }
        
        monkeypatch.setattr(
            intrusion_api.IntrusionService,
            "__init__",
            fake_init,
        )
        monkeypatch.setattr(
            intrusion_api.IntrusionService,
            "check_intrusion",
            fake_check_intrusion,
        )

        response = client.post(
            "/intrusion/check",
            json=valid_network_payload(),
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200

        data = response.json()

        assert data["intrusion"] is True
        assert data["attack_probability"] == 0.91
        assert data["detection_source"] == "rule_engine"
        assert data["detection_reason"] == "Possible packet flood attack"
        assert data["event_id"] == 1
        assert data["alert_id"] == 1

def test_autoencoder_check_returns_expected_response_for_admin(
        client,
        db_session,
        monkeypatch,
):
        from app.api.v1 import autoencoder as autoencoder_api

        token = create_admin_token(
             client,
             db_session,
             "admin-autoencoder-response@example.com"
        )

        def fake_init(self, event_repo, alert_repo):
             pass

        def fake_check_anomaly(self, payload):
             return {
                  "anomaly": True,
                  "anomaly_score": 23.59,
                  "raw_anomaly_score": 9.58,
                  "reconstruction_error": 0.131,
                  "threshold": 0.013,
                  "severity": "medium",
                  "risk_score": 23,
                  "event_id":15,
                  "alert_id": 11,
             }

        monkeypatch.setattr(
             autoencoder_api.AutoencoderService,
             "__init__",
             fake_init,
        )

        monkeypatch.setattr(
             autoencoder_api.AutoencoderService,
             "check_anomaly",
             fake_check_anomaly,
        )        

        response = client.post(
             "/autoencoder/check",
             json=valid_network_payload(),
             headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200

        data = response.json()

        assert data["anomaly"] is True
        assert data["anomaly_score"] == 23.59
        assert data["raw_anomaly_score"] == 9.58
        assert data["reconstruction_error"] == 0.131
        assert data["threshold"] == 0.013
        assert data["severity"] == "medium"
        assert data["risk_score"] == 23
        assert data["event_id"] == 15
        assert data["alert_id"] == 11