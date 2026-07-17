def test_search_flights(test_client):
    response = test_client.get("/reports/flights")

    assert response.status_code == 200


def test_booking_reports(test_client, admin_token):
    response = test_client.get(
        "/reports/bookings",
        headers=admin_token,
    )

    assert response.status_code == 200


def test_history(test_client, passenger_token):
    response = test_client.get(
        "/reports/history",
        headers=passenger_token,
    )

    assert response.status_code == 200