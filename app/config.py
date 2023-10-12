from pydantic.v1 import BaseSettings, root_validator


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @root_validator
    def get_database_url(cls, value):
        """Получаем новую переменную DATABASE_URL."""
        value["DATABASE_URL"] = (
            f"postgresql+asyncpg://{value['DB_USER']}:"
            f"{value['DB_PASS']}@{value['DB_HOST']}:"
            f"{value['DB_PORT']}/{value['DB_NAME']}"
        )
        return value

    class Config:
        env_file = ".env"


settings = Settings()

print(settings.DATABASE_URL)
