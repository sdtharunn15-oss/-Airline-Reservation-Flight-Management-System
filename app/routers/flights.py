from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Flight
from app.schemas import FlightCreate, FlightUpdate, FlightResponse
from app.dependencies import admin_only

router = APIRouter(
    prefix="/flights",
    tags=["Flights"]
)

@router.post("/", response_model=FlightResponse)
def create_flight(
    flight: FlightCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    existing = db.query(Flight).filter(
        Flight.flight_number == flight.flight_number
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Flight number already exists"
        )

    new_flight = Flight(**flight.model_dump())

    db.add(new_flight)
    db.commit()
    db.refresh(new_flight)

    return new_flight

@router.get("/", response_model=list[FlightResponse])
def get_flights(
    db: Session = Depends(get_db)
):
    return db.query(Flight).all()

@router.get("/{flight_id}", response_model=FlightResponse)
def get_flight(
    flight_id: int,
    db: Session = Depends(get_db)
):
    flight = db.query(Flight).filter(
        Flight.id == flight_id
    ).first()

    if not flight:
        raise HTTPException(
            status_code=404,
            detail="Flight not found"
        )

    return flight

@router.put("/{flight_id}", response_model=FlightResponse)
def update_flight(
    flight_id: int,
    flight: FlightUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    db_flight = db.query(Flight).filter(
        Flight.id == flight_id
    ).first()

    if not db_flight:
        raise HTTPException(
            status_code=404,
            detail="Flight not found"
        )

    duplicate = db.query(Flight).filter(
        Flight.flight_number == flight.flight_number,
        Flight.id != flight_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Flight number already exists"
        )

    for key, value in flight.model_dump().items():
        setattr(db_flight, key, value)

    db.commit()
    db.refresh(db_flight)

    return db_flight

@router.delete("/{flight_id}")
def delete_flight(
    flight_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_only)
):
    flight = db.query(Flight).filter(
        Flight.id == flight_id
    ).first()

    if not flight:
        raise HTTPException(
            status_code=404,
            detail="Flight not found"
        )

    db.delete(flight)
    db.commit()

    return {"message": "Flight deleted successfully"}