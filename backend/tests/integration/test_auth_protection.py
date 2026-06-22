def test_users_me_requires_authentication(client):
    response = client.get("users/me")

    assert response.status_code in [401, 403]

def test_users_list_requires_authentication(client):
    response = client.get("/users/")

    assert response.status_code in [401, 403]

def    test_alerts_requires_authentication(client):
    response = client.get("/alerts/")

def test_intrusion_check_requires_authentication(client):
    payload = {
        "source_ip": "185.220.101.1",
        "destination_ip": "10.0.0.5",
        "protocol": "TCP",
        "duration": 1,
        "bytes_sent": 60000,
        "bytes_received": 10,
        "packets_sent": 1200,
        "packets_received": 1,
    }

    response = client.post("/intrusion/check", json=payload)

    assert response.status_code in [401, 403]

def test_autoencoder_check_requires_authentication(client):
    payload = {
        "source_ip": "185.220.101.1",
        "destination_ip": "10.0.0.5",
        "protocol": "TCP",
        "duration": 1,
        "bytes_sent": 60000,
        "bytes_received": 10,
        "packets_sent": 1200,
        "packets_received": 1,
    }             

    response = client.post("/autoencoder/check", json=payload)

    assert response.status_code in [401, 403]