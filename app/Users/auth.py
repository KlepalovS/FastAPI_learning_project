from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.users.dao import UsersDAO


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    """Получает захэшированную строку с паролем."""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    """
    Проверяет соответствие введенного пароля с захэшированным и
    возвращает True, если значения совпадают, иначе - False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Создает access токен. Алгоритм работы функции описан ниже.
    Сперва копирует исходные данные в переменную to_encode для
    дальнейшей работы с этими данными. Затем создает время жизни
    токена expire и добавляет его к данным, хранящимся в переменной
    to_encode. Затем получает и возвращает полученный токен.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_LIFETIME
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)


async def authenticate_user(email: EmailStr, password: str):
    """
    Возвращает аутентифицированного пользователя, если пользователь
    с такой почтой существует и пароль совпадает.
    """
    user = await UsersDAO.get_one_or_none(email=email)
    if not user and not verify_password(password, user.password):
        return None
    return user
