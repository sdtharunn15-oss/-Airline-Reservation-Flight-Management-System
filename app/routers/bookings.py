from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Booking, Flight
from app.schemas import BookingCreate, BookingUpdate, BookingResponse
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)




@router.post("/", response_model=BookingResponse)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role != "Passenger":
        raise HTTPException(
            status_code=403,
            detail="Only passengers can book flights"
        )

    if booking.journey_date < date.today():
        raise HTTPException(
            status_code=400,
            detail="Journey date cannot be in the past"
        )

    flight = db.query(Flight).filter(
        Flight.id == booking.flight_id
    ).first()

    if not flight:
        raise HTTPException(
            status_code=404,
            detail="Flight not found"
        )

    seat = db.query(Booking).filter(
        Booking.flight_id == booking.flight_id,
        Booking.journey_date == booking.journey_date,
        Booking.seat_number == booking.seat_number,
        Booking.booking_status != "Cancelled"
    ).first()

    if seat:
        raise HTTPException(
            status_code=400,
            detail="Seat already booked"
        )

    new_booking = Booking(
        passenger_id=current_user.id,
        flight_id=booking.flight_id,
        journey_date=booking.journey_date,
        seat_number=booking.seat_number,
        booking_status="Booked"
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking

@router.get("/", response_model=list[BookingResponse])
def get_bookings(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if current_user.role == "Admin":
        return db.query(Booking).all()

    return db.query(Booking).filter(
        Booking.passenger_id == current_user.id
    ).all()


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: int,
    db: Session =Depends(get_db),
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

    return booking

@router.put("/{booking_id}", response_model=BookingResponse)
def update_booking(
    booking_id: int,
    booking_update: BookingUpdate,
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

    booking.booking_status = booking_update.booking_status

    db.commit()
    db.refresh(booking)

    return booking


