import httpx

from backend.app.core.config import get_settings
from backend.app.core.providers.base import BaseLLMProvider
from backend.app.schemas.llm_response import LLMResponse


class OllamaProvider(BaseLLMProvider):
    """
    LLM Provider implementation for Ollama.
    """

    def __init__(self):
        self.settings = get_settings()

        self.base_url = self.settings.ollama_base_url.rstrip("/")
        self.model = self.settings.ollama_model
        self.timeout = self.settings.ollama_timeout
        self.temperature = self.settings.ollama_temperature
        print("Loaded Base URL:", self.base_url)
        print("Loaded Model:", self.model)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMResponse:

        prompt = f"{system_prompt}\n\n{user_prompt}"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature
            }
        }

        try:
            print("=" * 60)
            print("OLLAMA URL:", f"{self.base_url}/api/generate")
            print("=" * 60)
            response = httpx.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()

            data = response.json()

            return LLMResponse(
                content=data.get("response", ""),
                model=self.model,
                provider="ollama",
                success=True,
            )

        except httpx.TimeoutException as exc:

            return LLMResponse(
                content="",
                model=self.model,
                provider="ollama",
                success=False,
                error=f"Request timed out: {exc}",
            )

        except httpx.HTTPError as exc:

            return LLMResponse(
                content="",
                model=self.model,
                provider="ollama",
                success=False,
                error=str(exc),
            )

        except Exception as exc:

            return LLMResponse(
                content="",
                model=self.model,
                provider="ollama",
                success=False,
                error=str(exc),
            )