import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL", "postgresql+asyncpg://postgres:pass@db:5432/telemed_scheduler"
    )

    SENTRY_DSN: str | None = None

    SECRET_KEY: str = os.environ.get(
        "SECRET_KEY",
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    APP_VERSION: str = "1.0"


settings = Config()
