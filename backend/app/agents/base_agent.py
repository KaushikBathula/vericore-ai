from abc import ABC, abstractmethod

from backend.app.core.llm_client import LLMClient


class BaseAgent(ABC):
    """
    Base class for all VeriCore AI agents.

    Every agent automatically receives access
    to the centralized LLM client.
    """

    def __init__(self, name: str):
        self.name = name
        self.llm = LLMClient()

    @abstractmethod
    def execute(self, input_data):
        """
        Execute the agent.
        Must be implemented by child classes.
        """
        raise NotImplementedError