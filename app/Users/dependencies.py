from datetime import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (IncorrectTokenFormatException,
                            NotAdminUserException, TokenAbsentException,
                            TokenExpiredException, UserNotFoundException)
from app.users.dao import UsersDAO
from app.users.models import Users


def get_token(request: Request):
    """
    Получает токен из куки.
    Если токена нет, то вызываем ошибку 401.
    """
    token = request.cookies.get('booking_access_token')
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    """Получает текущего пользователя по access токену."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormatException
    expire: str = payload.get('exp')
    if (not expire) or (int(expire) < float(datetime.utcnow().timestamp())):
        raise TokenExpiredException
    user_id: str = payload.get('sub')
    if not user_id:
        raise UserNotFoundException
    user = await UsersDAO.get_by_id(int(user_id))
    if not user:
        raise UserNotFoundException
    return user


async def get_current_admin_user(
    current_user: Users = Depends(get_current_user)
):
    """
    Возвращает текущего пользователя, если он является администратором.
    Иначе вызывает ошибку 401. Необходимо реализовать роли для пользователей
    Для корректной работы ф-ии.
    """
    # if current_user.role != "admin":
    #   raise NotAdminUserException
    return current_user
