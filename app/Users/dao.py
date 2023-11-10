from app.services.base import BaseDAO
from app.users.models import Users


class UsersDAO(BaseDAO):
    """
    Объект для работы с данными пользователей.
    """

    model = Users
