"""
RegRadar — Application Configuration
Centralised settings loaded from environment variables via pydantic-settings.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """All application settings — sourced from .env file or env vars."""

    # ── Application ──────────────────────────────────────────────────
    APP_NAME: str = "RegRadar"
    APP_ENV: str = "development"
    LOG_LEVEL: str = "DEBUG"
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    # ── Database ─────────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://regradar:regradar_secret@localhost:5432/regradar"
    DATABASE_URL_SYNC: str = "postgresql://regradar:regradar_secret@localhost:5432/regradar"

    # ── Redis / Celery ───────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # ── LLM ──────────────────────────────────────────────────────────
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    LLM_PROVIDER: str = "openai"  # "openai" | "anthropic"
    LLM_MODEL: str = "gpt-4o"

    # ── Auth / Security ──────────────────────────────────────────────
    SECRET_KEY: str = "change-this-to-a-random-64-char-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24h

    # ── Alert Delivery ───────────────────────────────────────────────
    SENDGRID_API_KEY: str = ""
    SENDGRID_FROM_EMAIL: str = "alerts@regradar.in"
    WHATSAPP_BSP_API_KEY: str = ""
    WHATSAPP_BSP_URL: str = "https://api.interakt.ai/v1/public/message/"

    # ── S3 / Object Storage ──────────────────────────────────────────
    S3_BUCKET_NAME: str = "regradar-documents"
    S3_ENDPOINT_URL: str = "https://s3.amazonaws.com"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "ap-south-1"

    # ── Proxy ────────────────────────────────────────────────────────
    PROXY_URL: str = ""

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()
