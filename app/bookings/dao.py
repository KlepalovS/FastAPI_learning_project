from app.bookings.models import Bookings
from app.services.base import BaseDAO


class BookingsDAO(BaseDAO):
    """Объект для работы с данными бронирований."""

    model = Bookings

    @classmethod
    async def add(cls):
        pass
