from datetime import date

from fastapi import APIRouter, Depends, Response

from app.hotels.schemas import SHotels


router = APIRouter(
    prefix='/hotels',
    tags=['Отели и номера'],
)


@router.get("/{location}")
async def get_hotels(
    location: str,
    date_from: date,
    date_to: date,
) -> list(SHotels):
    """
    Возвращает список отелей по заданой локации.
    Отель возвращается только, если в указаных датах
    есть хоть один свободный номер.
    """
    return await HotelsDAO.get_all()
