from abc import ABC, abstractmethod

from app.schemas.llm_response import LLMResponse


class BaseLLMProvider(ABC):

    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMResponse:
        pass