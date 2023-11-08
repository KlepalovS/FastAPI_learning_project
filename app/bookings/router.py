from fastapi import APIRouter

from app.bookings.dao import BookingsDAO


router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования'],
)


@router.get("")
async def get_bookings():
    """Эндпоинт для получения всех бронирований."""
    return await BookingsDAO.get_all()
