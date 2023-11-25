from datetime import date

from fastapi import APIRouter, Depends

from app.bookings.dao import BookingsDAO
from app.bookings.schemas import SBooking
from app.exceptions import BookingNotFound, RoomCanNotBeBooked
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
    """Эндпоинт для получения всех бронирований пользователя."""
    return await BookingsDAO.get_all(user_id=user.id)


@router.post("")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    """Эндпоинт для добавления бронирования."""
    booking = await BookingsDAO.add(
        user.id,
        room_id,
        date_from,
        date_to,
    )
    if not booking:
        raise RoomCanNotBeBooked


@router.delete("/{booking_id}")
async def delete_booking(
    booking_id: int,
    user: Users = Depends(get_current_user),
):
    """Эндпоинт для удаления бронирования у пользователя."""
    booking = await BookingsDAO.get_by_id(booking_id)
    if not booking:
        raise BookingNotFound
    await BookingsDAO.delete(user_id=user.id, booking_id=booking_id)
