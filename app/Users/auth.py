from passlib.context import CryptContext


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
