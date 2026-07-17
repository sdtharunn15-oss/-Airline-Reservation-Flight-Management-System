from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import Booking

router = APIRouter(
    prefix="",
    tags=["Boarding"]
)

@router.post("/checkin/{booking_id}")
def checkin(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if current_user.role == "Passenger" and booking.passenger_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    departure = booking.flight.departure_time

    if datetime.now() < departure - timedelta(hours=24):
        raise HTTPException(
            status_code=400,
            detail="Check-in allowed only within 24 hours before departure"
        )

    booking.checked_in = True

    db.commit()

    return {
        "message": "Check-in successful"
    }

@router.post("/boarding/{booking_id}")
def board_flight(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    if not booking.checked_in:
        raise HTTPException(
            status_code=400,
            detail="Passenger has not checked in"
        )

    booking.boarded = True
    booking.booking_status = "Completed"

    db.commit()

    return {
        "message": "Passenger boarded successfully"
    }


@router.get("/passengers/{passenger_id}/bookings")
def passenger_history(
    passenger_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role == "Passenger" and current_user.id != passenger_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    bookings = db.query(Booking).filter(
        Booking.passenger_id == passenger_id
    ).all()

    return bookings


