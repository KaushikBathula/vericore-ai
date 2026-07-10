from backend.app.core.config import Settings, get_settings


def get_app_settings() -> Settings:
    """Provide application settings to FastAPI dependencies."""
    return get_settings()
