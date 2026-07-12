"""
Application configuration.

All configuration is loaded from environment variables via Pydantic Settings,
per SAGE_BLUEPRINT.md Section 89 (Configuration Management).

Never hardcode secrets here. Real values belong in a local, untracked .env file;
.env.example documents the required keys with placeholders only.
"""
from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application settings, sourced from environment variables."""

    model_config = SettingsConfigDict(
        # Checks both locations because env_file paths are resolved relative
        # to the process's current working directory: ".env" covers running
        # `uvicorn` from the repo root, "../.env" covers running it from
        # backend/ (as this README's non-Docker instructions do). Missing
        # files are silently skipped, and real environment variables (e.g.
        # those Docker Compose injects via `env_file:`) always take priority
        # over both.
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Application ---
    APP_NAME: str = "Sage"
    APP_ENV: str = Field(default="development")  # development | production | test
    APP_DEBUG: bool = Field(default=True)
    API_V1_PREFIX: str = "/api/v1"

    # --- Server ---
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # --- CORS ---
    CORS_ORIGINS: List[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    # --- Database ---
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://sage_user:sage_password@localhost:5432/sage_db"
    )
    DATABASE_ECHO: bool = Field(default=False)

    # --- AI Providers (Phase 2 will consume these; declared now per Section 89) ---
    GEMINI_API_KEY: str = Field(default="")
    OPENAI_API_KEY: str = Field(default="")
    CLAUDE_API_KEY: str = Field(default="")
    OPENROUTER_API_KEY: str = Field(default="")
    DEFAULT_AI_PROVIDER: str = Field(default="gemini")

    # --- Search Provider (Phase 5) ---
    TAVILY_API_KEY: str = Field(default="")

    # --- Storage ---
    STORAGE_PATH: str = Field(default="/app/storage/files")
    MAX_UPLOAD_SIZE_MB: int = Field(default=25)

    # --- Logging ---
    LOG_LEVEL: str = Field(default="INFO")
    LOG_DIR: str = Field(default="logs")

    # --- Security ---
    SECRET_KEY: str = Field(default="change-me-in-env")

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def split_cors_origins(cls, value):
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (loaded once per process)."""
    return Settings()
