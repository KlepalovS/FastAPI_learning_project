from datetime import date

from sqlalchemy import and_, func, insert, or_, select

from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.services.base import BaseDAO


class HotelsDAO(BaseDAO):
    """Обьект для работы с данными отелей."""

    model = Hotels
