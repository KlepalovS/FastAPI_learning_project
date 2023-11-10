from pydantic import BaseModel, EmailStr


class SUserRegister(BaseModel):
    """
    Pydantic схема для регистрации пользователя.
    """

    email: EmailStr
    password: str
