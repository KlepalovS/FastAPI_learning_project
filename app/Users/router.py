from fastapi import APIRouter, HTTPException, Response, status

from app.users.auth import (
    authenticate_user, create_access_token, get_password_hash
)
from app.users.dao import UsersDAO
from app.users.schemas import SUserAuth


router = APIRouter(
    prefix='/auth',
    tags=['Auth и Пользователи'],
)


@router.post('/register')
async def register_user(user_data: SUserAuth):
    """
    Эндпоинт, осуществляющий регистрацию нового пользователя.
    Принимает пользовательские данные (логин(почта) и пароль).
    Проверяет существует ли такой пользователь, если пользователь
    уже существует, то рейзит ошибку 500. Если пользователя с
    такой почтой не существует - хэширует пароль и добавляет
    нового пользователя с введенной почтой и захэшированным паролем.
    """
    existing_user = await UsersDAO.get_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    """
    Эндпоинт, осуществляющий логин пользователя в системе.
    Принимает пользовательские данные (почта и пароль).
    Получает пользователя с указанными данными, если пользователь
    не существует, то рейзит ошибку 401. Получает и возвращает
    access_token для данного пользователя. Заносит токен в куки.
    """
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}