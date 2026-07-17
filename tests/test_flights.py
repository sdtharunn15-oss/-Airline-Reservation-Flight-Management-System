def test_create_flight(test_client, admin_token):
    response = test_client.post(
        "/flights/",
        headers=admin_token,
        json={
            "flight_number": "AI101",
            "airline_name": "Air India",
            "source": "Chennai",
            "destination": "Delhi",
            "departure_time": "2026-08-15T09:00:00",
            "arrival_time": "2026-08-15T11:30:00",
            "total_seats": 180,
        },
    )

    assert response.status_code == 200


def test_get_flights(test_client):
    response = test_client.get("/flights/")

    assert response.status_code == 200