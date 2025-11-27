from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    APP_NAME: str = "RateMyMP API"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api"

    DATABASE_URL: str = Field(
        default="postgresql+psycopg2://ratemymp:ratemymp@postgres:5432/ratemymp",
        description="SQLAlchemy connection string",
    )
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10

    ALEMBIC_CONFIG: str = "alembic.ini"

    CORS_ALLOWED_ORIGINS: List[str] = Field(default_factory=lambda: ["*"])

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> "Settings":
    return Settings()


settings = get_settings()
