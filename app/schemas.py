from datetime import datetime, date
from pydantic import BaseModel, EmailStr


# ===========================
# Authentication Schemas
# ===========================

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# ===========================
# Flight Schemas
# ===========================

class FlightCreate(BaseModel):
    flight_number: str
    airline_name: str
    source: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    total_seats: int


class FlightUpdate(BaseModel):
    flight_number: str
    airline_name: str
    source: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    total_seats: int


class FlightResponse(BaseModel):
    id: int
    flight_number: str
    airline_name: str
    source: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    total_seats: int

    class Config:
        from_attributes = True


# ===========================
# Booking Schemas
# ===========================

class BookingCreate(BaseModel):
    flight_id: int
    journey_date: date
    seat_number: str


class BookingUpdate(BaseModel):
    booking_status: str


class BookingResponse(BaseModel):
    id: int
    passenger_id: int
    flight_id: int
    journey_date: date
    seat_number: str
    booking_status: str
    checked_in: bool
    boarded: bool

    class Config:
        from_attributes = True