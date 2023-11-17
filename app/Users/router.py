from fastapi import APIRouter, Depends, Response

from app.exceptions import (IncorrectEmailOrPasswordException,
                            UserAlreadyExistsException)
from app.users.auth import (authenticate_user, create_access_token,
                            get_password_hash)
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_admin_user, get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth

router = APIRouter(
    prefix='/auth',
    tags=['Auth и Пользователи'],
)


@router.post('/register')
async def register_user(user_data: SUserAuth) -> None:
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
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth) -> dict:
    """
    Эндпоинт, осуществляющий логин пользователя в системе.
    Принимает пользовательские данные (почта и пароль).
    Получает пользователя с указанными данными, если пользователь
    не существует, то рейзит ошибку 401. Получает и возвращает
    access_token для данного пользователя. Заносит токен в куки.
    """
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post('/logout')
async def logout_user(response: Response) -> dict:
    """
    Эндпоинт для выхода пользователя из системы.
    Удаляет access токен из куки.
    """
    response.delete_cookie("booking_access_token")
    return {"message": "Пользователь вышел из системы."}


@router.get("/me")
async def get_users_me(
    current_user: Users = Depends(get_current_user)
):
    """Эндпоинт,который возвращает текущего пользователя."""
    return current_user


@router.get("/all")
async def get_all_users(
    current_user: Users = Depends(get_current_admin_user)
):
    """
    Эндпоинт,который возвращает всех пользователей имеющихся в системе.
    Необходимо для работы администратора. Для корректной работы необходимо
    реализвовать наличие поля роли для пользователя.
    """
    return await UsersDAO.get_all()
