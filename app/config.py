import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str

    SENTRY_DSN: str | None = None

    # CORS_ORIGINS: list[str]
    # CORS_ORIGINS_REGEX: str | None = None
    # CORS_HEADERS: list[str]

    APP_VERSION: str = "1.0"


DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql+asyncpg://postgres:pass@db:5432/telemed_scheduler"
)

settings = Config(DATABASE_URL=DATABASE_URL)
