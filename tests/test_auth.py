def test_register(test_client):
    response = test_client.post(
        "/auth/register",
        json={
            "username": "admin",
            "email": "admin@test.com",
            "password": "admin123",
            "role": "Admin"
        }
    )

    assert response.status_code == 200


def test_login(test_client):
    test_client.post(
        "/auth/register",
        json={
            "username": "admin",
            "email": "admin@test.com",
            "password": "admin123",
            "role": "Admin"
        }
    )

    response = test_client.post(
        "/auth/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()