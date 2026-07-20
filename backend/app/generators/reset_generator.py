"""
Reset Generator

Generates automatic reset initialization logic for Verilog
testbenches.
"""

from __future__ import annotations

from backend.app.generators.base_generator import BaseGenerator
from backend.app.schemas.port import Port
from backend.app.schemas.requirement_spec import RequirementSpec


RESET_SIGNAL_NAMES: set[str] = {
    "rst",
    "reset",
    "reset_n",
    "rst_n",
}


class ResetGenerator(BaseGenerator):
    """
    Generates reset initialization logic.
    """

    def get_reset_signal(
        self,
        requirement: RequirementSpec,
    ) -> Port | None:
        """
        Detect the reset input signal.

        Parameters
        ----------
        requirement:
            Parsed hardware requirement.

        Returns
        -------
        Port | None
            Matching reset input if found.
        """

        for port in requirement.inputs:
            if port.signal_name.lower() in RESET_SIGNAL_NAMES:
                return port

        return None

    def generate(
        self,
        requirement: RequirementSpec,
    ) -> list[str]:
        """
        Generate reset initialization.

        Parameters
        ----------
        requirement:
            Parsed hardware requirement.

        Returns
        -------
        list[str]
            Verilog reset initialization.
        """

        reset = self.get_reset_signal(requirement)

        if reset is None:
            return []

        lines: list[str] = []

        active_low = reset.signal_name.lower().endswith("_n")

        lines.append("initial begin")

        if active_low:
            lines.append(f"    {reset.signal_name} = 0;")
        else:
            lines.append(f"    {reset.signal_name} = 1;")

        lines.append("end")

        self.add_blank_line(lines)

        return lines