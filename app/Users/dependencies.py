from datetime import datetime
from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError

from app.config import settings
from app.users.dao import UsersDAO


def get_token(request: Request):
    """
    Получает токен из куки.
    Если токена нет, то вызываем ошибку 401.
    """
    token = request.cookies.get('booking_access_token')
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='В куки нет токена!',
        )
    return token


async def get_current_user(token: str = Depends(get_token)):
    """Получает текущего пользователя по access токену."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Токен не является JWT!',
        )
    expire: str = payload.get('exp')
    if (not expire) or (int(expire) < float(datetime.utcnow().timestamp())):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Время действия access токена истекло!',
        )
    user_id: str = payload.get('sub')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User_id не получен из JWT!',
        )
    user = await UsersDAO.get_by_id(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Пользователь с {user_id} не найден в БД!',
        )
    return user
