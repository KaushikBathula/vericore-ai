"""
Clock Generator

Generates automatic clock initialization and clock generation
logic for Verilog testbenches.

A clock signal is automatically detected from the DUT inputs
using the configured clock signal names.
"""

from __future__ import annotations

from backend.app.generators.base_generator import BaseGenerator
from backend.app.generators.constants import (
    CLOCK_SIGNAL_NAMES,
    DEFAULT_CLOCK_HALF_PERIOD,
)
from backend.app.schemas.port import Port
from backend.app.schemas.requirement_spec import RequirementSpec


class ClockGenerator(BaseGenerator):
    """
    Generates clock initialization and clock toggling logic.
    """

    def get_clock_signal(
        self,
        requirement: RequirementSpec,
    ) -> Port | None:
        """
        Detect the DUT clock input.

        Parameters
        ----------
        requirement:
            Parsed hardware requirement.

        Returns
        -------
        Port | None
            Matching clock input if found.
        """

        for port in requirement.inputs:
            if port.signal_name.lower() in CLOCK_SIGNAL_NAMES:
                return port

        return None

    def generate(
        self,
        requirement: RequirementSpec,
    ) -> list[str]:
        """
        Generate Verilog clock generation logic.

        Parameters
        ----------
        requirement:
            Parsed hardware requirement.

        Returns
        -------
        list[str]
            Verilog source lines. Returns an empty list if
            no clock signal exists.
        """

        clock = self.get_clock_signal(requirement)

        if clock is None:
            return []

        lines: list[str] = []

        # ---------------------------------------------
        # Clock Initialization
        # ---------------------------------------------

        lines.append("initial begin")
        lines.append(f"    {clock.signal_name} = 0;")
        lines.append("end")
        self.add_blank_line(lines)

        # ---------------------------------------------
        # Clock Generation
        # ---------------------------------------------

        lines.append(
            f"always #{DEFAULT_CLOCK_HALF_PERIOD}"
        )
        lines.append(
            f"    {clock.signal_name} = ~{clock.signal_name};"
        )
        self.add_blank_line(lines)

        return lines