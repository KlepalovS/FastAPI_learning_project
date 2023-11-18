from fastapi import HTTPException, status


class BookingException(HTTPException):
    """
    Базовый класс исключений в приложении,
    наследуемый от класса HTTPException.
    Задаем значения по умолчанию (500 код без деталей).
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    """Класс исключения, когда пользователь уже существует в БД."""

    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует!"


class IncorrectEmailOrPasswordException(BookingException):
    """Класс исключения, когда введены неверные почта или пароль."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверные почта или пароль!"


class TokenAbsentException(BookingException):
    """Класс исключения, когда токена нет в куки."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "В куки нет токена!"


class TokenExpiredException(BookingException):
    """Класс исключения, когда истекло время действия токена."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Время действия токена истекло!"


class IncorrectTokenFormatException(BookingException):
    """Класс исключения, когда полученный токен неверного формата."""

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена!"


class UserNotFoundException(BookingException):
    """Класс исключения, когда нет user_id или пользователя."""

    status_code = status.HTTP_401_UNAUTHORIZED


class NotAdminUserException(BookingException):
    """
    Класс исключения, когда пользователь, не являясь админом,
    пытается получить доступ к ресурсу, доступному только админу.
    """

    status_code = status.HTTP_403_FORBIDDEN
    detail = 'Доступ запрещен! Пользователь с не админ!'
