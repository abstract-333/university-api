import os
from typing import Final, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

MINUTE: Final[int] = 60
HOUR: Final[int] = MINUTE * 60
DAY: Final[int] = HOUR * 24
MONTH: Final[int] = DAY * 30

# To make alembic finds path correctly
additional_path: str = ""
if os.path.exists("src/"):
    additional_path = "src/"


class Settings(BaseSettings):
    """There fields are rewritten by env file"""

    # Mode
    MODE: Literal["LOCAL", "TEST", "PROD"] = "PROD"

    # JWT
    JWT_SECRET_KEY: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_ACCESS_TOKEN: int = MONTH
    JWT_EXPIRATION_REFRESH_TOKEN: int = MONTH

    # Server
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000

    # Number of Sessions
    SESSIONS_NUMBER: int = 5

    # DB PostgreSQL
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # Sentry
    SENTRY_URL: str

    # SMTP
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 465

    # Yandex
    YANDEX_API: str

    # NanoID
    SIZE: int = 10

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?async_fallback=True"

    """If .env.local.local exists it will load it.
    Otherwise load .env.local.prod"""
    model_config = SettingsConfigDict(
        # To make alembic finds path correctly
        env_file=(
            f"{additional_path}settings/.env.prod",
            f"{additional_path}settings/.env.local",
        ),
        env_file_encoding="utf-8",
    )


settings_obj: Settings = Settings()
