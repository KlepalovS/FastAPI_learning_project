from sqlalchemy import JSON, Column, ForeignKey, Integer, String
from app.database import Base


class Rooms(Base):
    """Модель для таблицы комнат."""

    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"))
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    services = Column(JSON)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)
