from functools import lru_cache
from pathlib import Path
from typing import Literal, cast, get_args

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

AIProvider = Literal[
    "openai",
    "anthropic",
    "google_gemini",
    "ollama",
    "azure_openai",
]


class Settings(BaseSettings):
    """Application settings loaded from environment variables and `.env`."""

    # ------------------------------------------------------------------
    # Application Configuration
    # ------------------------------------------------------------------

    database_url: str = Field(
        default="sqlite:///./vericore.db",
        alias="DATABASE_URL",
    )

    log_level: str = Field(
        default="INFO",
        alias="LOG_LEVEL",
    )

    project_root: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parents[3],
        alias="PROJECT_ROOT",
    )

    generated_project_path: Path = Field(
        default=Path("generated_projects"),
        alias="GENERATED_PROJECT_PATH",
    )

    api_prefix: str = Field(
        default="",
        alias="API_PREFIX",
    )

    debug: bool = Field(
        default=False,
        alias="DEBUG",
    )

    secret_key: str = Field(
        default="change-this-development-secret",
        alias="SECRET_KEY",
    )

    # ------------------------------------------------------------------
    # AI Provider
    # ------------------------------------------------------------------

    ai_provider: AIProvider = Field(
        default="ollama",
        alias="AI_PROVIDER",
    )

    # ------------------------------------------------------------------
    # Ollama Configuration
    # ------------------------------------------------------------------

    ollama_base_url: str = Field(
        default="http://localhost:11434",
        alias="OLLAMA_BASE_URL",
    )

    ollama_model: str = Field(
        default="qwen2.5:3b",
        alias="OLLAMA_MODEL",
    )

    ollama_temperature: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0,
        alias="OLLAMA_TEMPERATURE",
    )

    ollama_timeout: float = Field(
        default=120.0,
        ge=1.0,
        alias="OLLAMA_TIMEOUT",
    )

    # ------------------------------------------------------------------
    # OpenAI Configuration (Future Support)
    # ------------------------------------------------------------------

    openai_api_key: str | None = Field(
        default=None,
        alias="OPENAI_API_KEY",
    )

    openai_model: str = Field(
        default="gpt-4.1-mini",
        alias="OPENAI_MODEL",
    )

    openai_temperature: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0,
        alias="OPENAI_TEMPERATURE",
    )

    openai_max_tokens: int = Field(
        default=4096,
        ge=1,
        alias="OPENAI_MAX_TOKENS",
    )

    openai_timeout: float = Field(
        default=60.0,
        ge=1.0,
        alias="OPENAI_TIMEOUT",
    )

    openai_max_retries: int = Field(
        default=3,
        ge=0,
        alias="OPENAI_MAX_RETRIES",
    )

    # ------------------------------------------------------------------
    # Settings Configuration
    # ------------------------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    # ------------------------------------------------------------------
    # Validators
    # ------------------------------------------------------------------

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        return value.upper()

    @field_validator("api_prefix")
    @classmethod
    def normalize_api_prefix(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            return ""
        return cleaned if cleaned.startswith("/") else f"/{cleaned}"

    @field_validator("ai_provider", mode="before")
    @classmethod
    def normalize_ai_provider(cls, value: str) -> AIProvider:
        normalized = value.strip().lower()

        if normalized not in get_args(AIProvider):
            raise ValueError(f"Unsupported AI provider: {value}")

        return cast(AIProvider, normalized)

    @field_validator("ollama_model")
    @classmethod
    def validate_ollama_model(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("OLLAMA_MODEL must not be empty.")

        return cleaned

    @field_validator("openai_model")
    @classmethod
    def validate_openai_model(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("OPENAI_MODEL must not be empty.")

        return cleaned

    # ------------------------------------------------------------------
    # Helper Properties
    # ------------------------------------------------------------------

    @property
    def generated_projects_dir(self) -> Path:
        if self.generated_project_path.is_absolute():
            return self.generated_project_path

        return self.project_root / self.generated_project_path

    @property
    def logs_dir(self) -> Path:
        return self.project_root / "logs"

    @property
    def outputs_dir(self) -> Path:
        return self.project_root / "outputs"


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()