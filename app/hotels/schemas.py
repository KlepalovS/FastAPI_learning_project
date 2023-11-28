from pydantic import BaseModel, Json


class SHotels(BaseModel):
    """Pydantic схема для работы с отелями."""

    id: int
    name: str
    location: str
    services: Json
    rooms_quantity: int
    image_id: int
    rooms_left: int

    class Config:
        orm_mode = True
