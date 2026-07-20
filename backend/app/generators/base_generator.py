"""
Base Generator

Provides common helper utilities shared by all Verilog
generation components.

Every specialized generator should inherit from this class
to maintain consistent formatting and avoid duplicated code.
"""

from __future__ import annotations


class BaseGenerator:
    """
    Base class for all Verilog generators.

    Provides reusable helper methods for building
    formatted Verilog source code.
    """

    @staticmethod
    def add_blank_line(lines: list[str]) -> None:
        """
        Append a blank line.
        """

        lines.append("")

    @staticmethod
    def append_block(
        lines: list[str],
        block: list[str],
    ) -> None:
        """
        Append an entire block of lines.
        """

        lines.extend(block)

    @staticmethod
    def indent_block(
        block: list[str],
        spaces: int = 4,
    ) -> list[str]:
        """
        Return an indented copy of a block.

        Parameters
        ----------
        block:
            List of source lines.

        spaces:
            Number of leading spaces.

        Returns
        -------
        list[str]
            Indented block.
        """

        prefix = " " * spaces

        return [
            prefix + line if line else ""
            for line in block
        ]

    @staticmethod
    def format_width(width: int) -> str:
        """
        Convert a signal width into Verilog bus syntax.

        Examples
        --------
        1  -> ""
        8  -> "[7:0] "
        32 -> "[31:0] "
        """

        if width <= 1:
            return ""

        return f"[{width - 1}:0] "

    @staticmethod
    def format_signal(
        signal_type: str,
        signal_name: str,
        signal_width: int,
    ) -> str:
        """
        Generate a Verilog signal declaration.

        Example
        -------
        reg clk;

        wire [7:0] data;
        """

        width = BaseGenerator.format_width(signal_width)

        return f"{signal_type} {width}{signal_name};"

    @staticmethod
    def begin_block(keyword: str) -> list[str]:
        """
        Generate a Verilog begin block.

        Example
        -------
        initial begin
        """

        return [
            f"{keyword} begin"
        ]

    @staticmethod
    def end_block() -> list[str]:
        """
        Generate a Verilog end block.
        """

        return [
            "end"
        ]