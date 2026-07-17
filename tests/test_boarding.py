from datetime import date, datetime, timedelta


def create_flight(test_client, admin_token):
    response = test_client.post(
        "/flights/",
        headers=admin_token,
        json={
            "flight_number": "AI201",
            "airline_name": "IndiGo",
            "source": "Chennai",
            "destination": "Mumbai",
            "departure_time": (datetime.now() + timedelta(hours=12)).isoformat(),
            "arrival_time": (datetime.now() + timedelta(hours=14)).isoformat(),
            "total_seats": 180
        },
    )
    return response.json()["id"]


def create_booking(test_client, passenger_token, flight_id):
    response = test_client.post(
        "/bookings/",
        headers=passenger_token,
        json={
            "flight_id": flight_id,
            "journey_date": str(date.today()),
            "seat_number": "B1"
        },
    )
    return response.json()["id"]


def test_checkin(test_client, admin_token, passenger_token):
    flight_id = create_flight(test_client, admin_token)
    booking_id = create_booking(test_client, passenger_token, flight_id)

    response = test_client.post(
        f"/checkin/{booking_id}",
        headers=passenger_token,
    )

    assert response.status_code == 200


def test_boarding(test_client, admin_token, passenger_token):
    flight_id = create_flight(test_client, admin_token)
    booking_id = create_booking(test_client, passenger_token, flight_id)

    test_client.post(
        f"/checkin/{booking_id}",
        headers=passenger_token,
    )

    response = test_client.post(
        f"/boarding/{booking_id}",
        headers=passenger_token,
    )

    assert response.status_code == 200