from datetime import date

from sqlalchemy import and_, func, insert, or_, select

from app.bookings.models import Bookings
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.services.base import BaseDAO


class BookingsDAO(BaseDAO):
    """Объект для работы с данными бронирований."""

    model = Bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        """
        Метод добавления нового бронирования пользователем.
        Сперва узнаем количество свободных номеров, затем,
        если количество номеров меньше 0 - возвращаем None,
        иначе добавляем бронирование в БД. Ниже приведен
        SQL запрос выполняемый алхимией.

        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = {room_id} AND
            (date_from >= {date_from} AND date_from <= {date_to}) OR
            (date_from <= {date_from} AND date_to > {date_from})
        )
        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        )
                    )
                )
            ).cte("booked_rooms")

            get_rooms_left = select(
                (
                    Rooms.quantity - func.count(booked_rooms.c.room_id)
                ).label("rooms_left")
            ).select_from(Rooms).join(
                booked_rooms,
                booked_rooms.c.room_id == Rooms.id,
                isouter=True,
            ).where(Rooms.id == 1).group_by(
                Rooms.quantity,
                booked_rooms.c.room_id,
            )

            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()

            if rooms_left <= 0:
                return None
            get_price = select(Rooms.price).filter_by(id=room_id)
            price = await session.execute(get_price)
            price: int = price.scalar()
            add_booking = insert(Bookings).values(
                room_id=room_id,
                user_id=user_id,
                date_from=date_from,
                date_to=date_to,
                price=price,
            ).returning(Bookings)

            new_booking = await session.execute(add_booking)
            await session.commit()
            return new_booking.scalar()

    @classmethod
    async def delete(
        cls,
        user_id: int,
        booking_id: int
    ):
        """
        Метод удаления бронирования текущего пользователя из БД.
        """
        pass
