from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Flight, Booking
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/flights")
def search_flights(
    source: str = None,
    destination: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Flight)

    if source:
        query = query.filter(Flight.source.ilike(f"%{source}%"))

    if destination:
        query = query.filter(Flight.destination.ilike(f"%{destination}%"))

    flights = query.offset((page - 1) * limit).limit(limit).all()

    return flights


@router.get("/bookings")
def booking_report(
    status: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    query = db.query(Booking)

    if current_user.role == "Passenger":
        query = query.filter(
            Booking.passenger_id == current_user.id
        )

    if status:
        query = query.filter(
            Booking.booking_status == status
        )

    return query.offset(
        (page - 1) * limit
    ).limit(limit).all()


@router.get("/history")
def booking_history(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    query = db.query(Booking)

    if current_user.role == "Passenger":
        query = query.filter(
            Booking.passenger_id == current_user.id
        )

    return query.offset(
        (page - 1) * limit
    ).limit(limit).all()


