"""
Configuration settings for the PyCode Platform.
"""

from typing import List
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""

    # Application
    APP_NAME: str = "PyCode Platform"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./pycode.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""

    # LLM provider
    LLM_PROVIDER: str = "groq"  # groq | openai | anthropic
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_API_KEY: str = ""
    HF_TOKEN: str = ""

    # JWT refresh
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Observability
    SENTRY_DSN: str = ""

    # CORS
    CORS_ORIGINS: str = (
        "http://localhost:5173,http://localhost:5174,http://localhost:3000"
    )

    # Frontend
    FRONTEND_URL: str = "http://localhost:5173"

    # Tutor
    TUTOR_PROMPT_FILE: str = "maestro_evaluador_de_codigo_python.txt"

    @property
    def cors_origins_list(self) -> List[str]:
        raw = [
            origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()
        ]
        if self.ENVIRONMENT == "production" and "*" in raw:
            raise RuntimeError("CORS wildcard prohibido en producción")
        return raw

    @property
    def project_root(self) -> Path:
        return Path(__file__).resolve().parents[3]

    @property
    def tutor_prompt_path(self) -> Path:
        return self.project_root / self.TUTOR_PROMPT_FILE

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
