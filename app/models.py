from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    DateTime
)
from sqlalchemy.orm import relationship

from app.database import Base
from sqlalchemy import Boolean

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    bookings = relationship("Booking", back_populates="passenger")


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, unique=True, nullable=False)
    airline_name = Column(String, nullable=False)
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    total_seats = Column(Integer, nullable=False)

    bookings = relationship("Booking", back_populates="flight")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    passenger_id = Column(Integer, ForeignKey("users.id"))
    flight_id = Column(Integer, ForeignKey("flights.id"))

    journey_date = Column(Date, nullable=False)
    seat_number = Column(String, nullable=False)
    booking_status = Column(String, default="Booked")

    passenger = relationship("User", back_populates="bookings")
    flight = relationship("Flight", back_populates="bookings")

    checked_in = Column(Boolean, default=False)
    boarded = Column(Boolean, default=False)