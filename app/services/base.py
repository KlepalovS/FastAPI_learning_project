from sqlalchemy import select

from app.database import async_session_maker


class BaseDAO:
    """Базовый объект для работы с данными."""

    model = None

    @classmethod
    async def get_all(cls):
        """Метод для получения всех экземпляров."""
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns)
            result = await session.execute(query)
            return result.mappings().all()
