from fastapi import APIRouter, HTTPException

from app.users.auth import get_password_hash
from app.users.dao import UsersDAO
from app.users.schemas import SUserRegister


router = APIRouter(
    prefix='/auth',
    tags=['Auth и Пользователи'],
)


@router.post('/register')
async def register_user(user_data: SUserRegister):
    """
    Функция, осуществляющая регистрацию нового пользователя.
    Принимает пользовательские данные (логин(почта) и пароль).
    Проверяет существует ли такой пользователь, если пользователь
    уже существует, то рейзит ошибку 500. Если пользователя с
    такой почтой не существует - хэширует пароль и добавляет
    нового пользователя с введенной почтой и захэшированным паролем.
    """
    existing_user = await UsersDAO.get_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=500)
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
