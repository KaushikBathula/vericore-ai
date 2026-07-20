"""
Signal Generator

Generates Verilog signal declarations for
testbench input and output ports.
"""

from __future__ import annotations

from backend.app.generators.base_generator import BaseGenerator
from backend.app.schemas.port import Port
from backend.app.schemas.requirement_spec import RequirementSpec


class SignalGenerator(BaseGenerator):
    """
    Generates signal declarations for a testbench.
    """

    def generate(
        self,
        requirement: RequirementSpec,
    ) -> list[str]:
        """
        Generate all signal declarations.

        Parameters
        ----------
        requirement:
            Parsed RTL requirement.

        Returns
        -------
        list[str]
            Verilog source lines.
        """

        lines: list[str] = []

        for port in requirement.inputs:
            lines.append(self._declare_input(port))

        if requirement.inputs:
            self.add_blank_line(lines)

        for port in requirement.outputs:
            lines.append(self._declare_output(port))

        if requirement.outputs:
            self.add_blank_line(lines)

        return lines

    def _declare_input(
        self,
        port: Port,
    ) -> str:
        """
        Generate an input declaration.

        Inputs are declared as reg in a testbench.
        """

        return self.format_signal(
            signal_type="reg",
            signal_name=port.signal_name,
            signal_width=port.signal_width,
        )

    def _declare_output(
        self,
        port: Port,
    ) -> str:
        """
        Generate an output declaration.

        Outputs are declared as wire.
        """

        return self.format_signal(
            signal_type="wire",
            signal_name=port.signal_name,
            signal_width=port.signal_width,
        )