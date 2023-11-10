from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    """
    Pydantic схема для регистрации пользователя,
    логирования пользователя.
    """

    email: EmailStr
    password: str
