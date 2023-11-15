from fastapi import APIRouter, Depends

from app.bookings.dao import BookingsDAO
from app.bookings.schemas import SBooking
from app.users.dependencies import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования'],
)


@router.get("")
async def get_bookings(
    user: Users = Depends(get_current_user)
) -> list[SBooking]:
    """Эндпоинт для получения всех бронирований."""
    return await BookingsDAO.get_all(user_id=user.id)
