import logging
import time

from app.core.config import get_settings
from app.core.providers.base import BaseLLMProvider
from app.core.providers.ollama_client import OllamaProvider
from app.schemas.llm_response import LLMResponse

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Central LLM gateway for VeriCore AI.

    Agents should communicate only with this class.
    """

    def __init__(self):
        self.settings = get_settings()
        self.provider = self._load_provider()
        self.max_retries = 3

    def _load_provider(self) -> BaseLLMProvider:
        """
        Load the configured LLM provider.
        """

        provider = self.settings.ai_provider

        if provider == "ollama":
            return OllamaProvider()

        raise ValueError(f"Unsupported AI provider: {provider}")

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMResponse:
        """
        Generate a response using the configured provider.

        Automatically retries transient failures before
        returning an error.
        """

        last_exception = None

        for attempt in range(1, self.max_retries + 1):

            try:
                logger.info(
                    "LLM request attempt %d/%d",
                    attempt,
                    self.max_retries,
                )

                response = self.provider.generate(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                )

                if response.success:
                    return response

                raise RuntimeError(
                    response.error or "Unknown LLM provider error."
                )

            except Exception as exc:

                last_exception = exc

                logger.warning(
                    "LLM request failed (attempt %d/%d): %s",
                    attempt,
                    self.max_retries,
                    exc,
                )

                if attempt < self.max_retries:
                    time.sleep(1)

        raise RuntimeError(
            f"LLM failed after {self.max_retries} attempts."
        ) from last_exception