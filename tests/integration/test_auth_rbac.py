from app.db.models.user import User


def test_register_user(client):
    payload = {
        "email": "user@example.com",
        "password": "Password123!",
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == payload["email"]
    assert data["role"] == "user"
    assert data["is_active"] is True
    assert "id" in data

def test_register_duplicate_user_returns_400(client):
    payload = {
        "email": "duplicate@example.com",
        "password": "Password123!",
    }

    first_response = client.post("/auth/register", json=payload)
    second_response = client.post("/auth/register", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 400

def test_login_user_returns_access_token(client):
    payload = {
        "email": "login@example.com",
        "password": "Password123!",
    }    

    client.post("/auth/register", json=payload)

    response = client.post("/auth/login", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 20

def test_login_with_wrong_password_returns_401(client):
    register_payload = {
        "email": "wrong-password@example.com",
        "password": "Password123!",
    }

    login_payload = {
        "email" : "wrong-password@example.com",
        "password": "WrongPassword123!",
    }

    client.post("/auth/register", json=register_payload)

    response = client.post("/auth/login", json=login_payload)

    assert response.status_code == 401

def test_users_me_returns_current_user_with_valid_token(client):
    payload = {
        "email": "me@example.com",
        "password": "Password123!",
    }

    client.post("/auth/register", json=payload)

    login_response = client.post("/auth/login", json=payload)
    token = login_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == payload["email"]
    assert data["role"] == "user"
    assert data["is_active"] is True

def test_regular_user_cannot_access_users_list(client):
    payload = {
        "email": "regular@example.com",
        "password": "Password123!",
    }    

    client.post("/auth/register", json=payload)

    login_response = client.post("/auth/login", json=payload)
    token = login_response.json()["access_token"]

    response = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403

def test_admin_can_access_users_list(client, db_session):
    payload = {
        "email": "admin@example.com",
        "password": "Password123!",
    }

    register_response = client.post("/auth/register", json=payload)
    user_id = register_response.json()["id"]

    admin_user = db_session.query(User).filter(User.id == user_id).first()
    admin_user.role = "admin"
    db_session.commit()

    login_response = client.post("/auth/login", json=payload)
    token = login_response.json()["access_token"]

    response = client.get(
        "/users/",
        headers={"Authorization": f"BEarer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) >= 1

    admin_emails = [user["email"] for user in data]
    assert payload["email"] in admin_emails