"""
Module Header Generator

Generates the module declaration for a Verilog testbench.
"""

from __future__ import annotations

from backend.app.generators.base_generator import BaseGenerator


class ModuleHeaderGenerator(BaseGenerator):
    """
    Generates the header for a testbench module.
    """

    def generate(
        self,
        testbench_name: str,
    ) -> list[str]:
        """
        Generate the module declaration.

        Parameters
        ----------
        testbench_name:
            Name of the generated testbench.

        Returns
        -------
        list[str]
            Verilog source lines.
        """

        lines: list[str] = []

        lines.append(f"module {testbench_name};")

        self.add_blank_line(lines)

        return lines