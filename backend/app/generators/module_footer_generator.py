"""
Module Footer Generator

Generates the closing statements for a Verilog module.
"""

from __future__ import annotations

from backend.app.generators.base_generator import BaseGenerator


class ModuleFooterGenerator(BaseGenerator):
    """
    Generates the footer for a Verilog module.
    """

    def generate(self) -> list[str]:
        """
        Generate the module footer.

        Returns
        -------
        list[str]
            Verilog source lines.
        """

        return [
            "endmodule",
        ]