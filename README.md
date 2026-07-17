Airline Reservation & Flight Management System

Airline Reservation & Flight Management System is a backend REST API developed using FastAPI. The application allows administrators to manage flights and enables passengers to register, log in, book flights, perform check-in, board flights, and view their booking history. The project uses JWT Authentication for secure access and SQLAlchemy with SQLite for database management.

Tech Stack

* Python 3.9+
* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT Authentication
* Passlib (bcrypt)
* Uvicorn
* Pytest

Features

Authentication

* User Registration
* User Login
* JWT Authentication
* Password Hashing
* Role-Based Authorization

User Roles

* Admin
* Passenger

Flight Management

* Create Flight
* View All Flights
* View Flight by ID
* Update Flight
* Delete Flight

Booking Management

* Create Booking
* View All Bookings
* View Booking by ID
* Update Booking Status

Boarding Management

* Passenger Check-in
* Passenger Boarding
* View Passenger Booking History

Reports

* Search Flights by Source and Destination
* Filter Bookings by Status
* Passenger Booking History
* Pagination Support

Business Rules

* Flight number must be unique.
* Journey date cannot be in the past.
* Seat number cannot be booked twice for the same flight and journey date.
* Check-in is allowed only within 24 hours before departure.
* Cancelled bookings release the reserved seat.
* Admin can manage flights and bookings.
* Passengers can access only their own bookings.

Project Structure

```
airline_reservation_system/
│
├── app/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── flights.py
│   │   ├── bookings.py
│   │   ├── boarding.py
│   │   └── reports.py
│   │
│   ├── auth.py
│   ├── database.py
│   ├── dependencies.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── utils.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_flights.py
│   ├── test_bookings.py
│   ├── test_boarding.py
│   └── test_reports.py
│
├── airline.db
├── requirements.txt
└── README.md
```

Installation

Clone the repository

```bash
git clone <repository_url>
```

Move into the project directory

```bash
cd airline_reservation_system
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

Install the required packages

```bash
pip install -r requirements.txt
```

Running the Application

Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

Application URL

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

ReDoc Documentation

```
http://127.0.0.1:8000/redoc
```

API Endpoints

Authentication

* POST /auth/register
* POST /auth/login

Flights

* POST /flights
* GET /flights
* GET /flights/{flight_id}
* PUT /flights/{flight_id}
* DELETE /flights/{flight_id}

Bookings

* POST /bookings
* GET /bookings
* GET /bookings/{booking_id}
* PUT /bookings/{booking_id}

Boarding

* POST /checkin/{booking_id}
* POST /boarding/{booking_id}
* GET /passengers/{passenger_id}/bookings

Reports

* GET /reports/flights
* GET /reports/bookings
* GET /reports/history

Running Tests

Execute all test cases using:

```bash
pytest
```

Generate Requirements File

```bash
pip freeze > requirements.txt
```

Author

Tharun
