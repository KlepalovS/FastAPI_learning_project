from fastapi import APIRouter

from app.bookings.dao import BookingsDAO
from app.bookings.schemas import SBooking


router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования'],
)


@router.get("")
async def get_bookings() -> list[SBooking]:
    """Эндпоинт для получения всех бронирований."""
    return await BookingsDAO.get_all()
