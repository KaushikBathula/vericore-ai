from langchain_openai import ChatOpenAI

from backend.app.core.config import get_settings

__all__ = ["get_llm"]


def _get_required_openai_api_key(api_key: str | None) -> str:
    """Return a validated OpenAI API key from settings."""
    if api_key is None or not api_key.strip():
        raise ValueError(
            "OPENAI_API_KEY must be configured when AI_PROVIDER is set to 'openai'."
        )
    return api_key.strip()


def _get_openai_llm() -> ChatOpenAI:
    """Build a LangChain ChatOpenAI instance from centralized settings."""
    settings = get_settings()
    api_key = _get_required_openai_api_key(settings.openai_api_key)

    return ChatOpenAI(
        api_key=api_key,
        model=settings.openai_model,
        temperature=settings.openai_temperature,
        max_tokens=settings.openai_max_tokens,
        timeout=settings.openai_timeout,
        max_retries=settings.openai_max_retries,
    )


def get_llm() -> ChatOpenAI:
    """Return the configured LangChain chat model for the active AI provider."""
    settings = get_settings()

    if settings.ai_provider == "openai":
        return _get_openai_llm()

    raise NotImplementedError(
        f"AI_PROVIDER '{settings.ai_provider}' is configured, but only 'openai' "
        "is implemented in the LLM factory."
    )
