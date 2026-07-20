"""
DUT Instantiator

Generates the DUT (Device Under Test) instantiation
for a Verilog testbench.
"""

from __future__ import annotations

from backend.app.generators.base_generator import BaseGenerator
from backend.app.schemas.requirement_spec import RequirementSpec


class DUTInstantiator(BaseGenerator):
    """
    Generates the DUT instantiation block.
    """

    def generate(
        self,
        requirement: RequirementSpec,
    ) -> list[str]:
        """
        Generate the DUT instantiation.

        Parameters
        ----------
        requirement:
            Parsed hardware requirement.

        Returns
        -------
        list[str]
            Verilog source lines.
        """

        lines: list[str] = []

        module_name = requirement.module_name

        lines.append(f"{module_name} dut (")

        ports = requirement.inputs + requirement.outputs

        for index, port in enumerate(ports):

            comma = "," if index < len(ports) - 1 else ""

            lines.append(
                f"    .{port.signal_name}({port.signal_name}){comma}"
            )

        lines.append(");")

        self.add_blank_line(lines)

        return lines