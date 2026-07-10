from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """Abstract lifecycle contract for future VeriCore AI agents."""

    @abstractmethod
    async def initialize(self) -> None:
        """Prepare resources needed before execution."""
        raise NotImplementedError

    @abstractmethod
    async def execute(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Execute the agent responsibility for the provided input."""
        raise NotImplementedError

    @abstractmethod
    async def validate(self, output_data: dict[str, Any]) -> bool:
        """Validate agent output before it enters the workflow state."""
        raise NotImplementedError

    @abstractmethod
    async def cleanup(self) -> None:
        """Release resources after execution."""
        raise NotImplementedError
