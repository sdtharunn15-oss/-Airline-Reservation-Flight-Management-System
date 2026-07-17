from fastapi import FastAPI

from app.database import Base, engine
from app import models

from app.routers import auth
from app.routers import auth, flights
from app.routers import auth, flights, bookings
from app.routers import auth, flights, bookings, boarding
from app.routers import auth, flights, bookings, boarding, reports
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Airline Reservation & Flight Management System"
)

app.include_router(auth.router)
app.include_router(flights.router)
app.include_router(bookings.router)
app.include_router(boarding.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {
        "message": "Airline Reservation & Flight Management System API"
    }