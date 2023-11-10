from sqlalchemy import insert, select

from app.database import async_session_maker


class BaseDAO:
    """Базовый объект для работы с данными."""

    model = None

    @classmethod
    async def get_by_id(cls, model_id: int):
        """
        Метод для получения экземпляра по id.
        Если экземпляр не получен - возвращает None.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        """
        Метод для получения одного экземпляра по заданым
        фильтрам, если такой имеется.
        Если экземпляр по фильтрам получить не удается - то
        возвращается None.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls, **filter_by):
        """Метод для получения всех экземпляров."""
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data):
        """Метод добавления данных в БД."""
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
