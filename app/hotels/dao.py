from datetime import date

from sqlalchemy import and_, func, insert, or_, select

from app.bookings.models import Bookings
from app.database import async_session_maker
from app.hotels.rooms.models import Rooms
from app.services.base import BaseDAO


class BookingsDAO(BaseDAO):

