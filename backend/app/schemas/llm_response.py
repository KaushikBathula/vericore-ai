from pydantic import BaseModel


class LLMResponse(BaseModel):
    """
    Standard response returned by every LLM provider.
    """

    content: str

    model: str

    provider: str

    success: bool = True

    error: str | None = None