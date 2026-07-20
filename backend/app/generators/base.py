"""
Abstract base classes for HDL generators.
"""

from abc import ABC, abstractmethod

from backend.app.schemas.rtl_design import RTLDesign

class HDLGenerator(ABC):
    """
    Base interface for all HDL code generators.

    Implementations convert an RTLDesign into HDL source code.
    """

    @abstractmethod
    def generate(self, rtl_design: RTLDesign) -> str:
        """
        Generate HDL source code from an RTLDesign.

        Args:
            rtl_design: Structured RTL representation.

        Returns:
            Generated HDL source code as a string.
        """
        raise NotImplementedError