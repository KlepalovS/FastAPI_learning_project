from datetime import date
from typing import Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel

from app.bookings.router import router as bookings_router
from app.users.router import router as users_router

app = FastAPI()

app.include_router(users_router)
app.include_router(bookings_router)


@app.get('/hotels')
def get_hotels(
    location: str,
    date_from: date,
    date_to: date,
    has_spa: Optional[bool] = None,
    stars: Optional[int] = Query(None, ge=1, le=5),
):
    return date_from, date_to


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post('/bookings')
def add_booking(booking: SBooking):
    pass
