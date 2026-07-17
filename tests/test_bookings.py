from datetime import date, timedelta


def create_flight(test_client, admin_token):
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
            "total_seats": 180
        },
    )
    return response.json()["id"]


def test_create_booking(test_client, admin_token, passenger_token):
    flight_id = create_flight(test_client, admin_token)

    response = test_client.post(
        "/bookings/",
        headers=passenger_token,
        json={
            "flight_id": flight_id,
            "journey_date": str(date.today() + timedelta(days=2)),
            "seat_number": "A1"
        },
    )

    assert response.status_code == 200
    assert response.json()["booking_status"] == "Booked"


def test_get_bookings(test_client, passenger_token):
    response = test_client.get(
        "/bookings/",
        headers=passenger_token
    )

    assert response.status_code == 200