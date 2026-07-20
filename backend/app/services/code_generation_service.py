"""
Code Generation Service.

Coordinates HDL artifact generation from an RTL design.
"""

from __future__ import annotations

from backend.app.generators.testbench_generator import TestbenchGenerator
from backend.app.generators.verilog_generator import VerilogGenerator
from backend.app.schemas.rtl_design import RTLDesign


class CodeGenerationService:
    """
    Coordinates HDL code generation.

    This service orchestrates the Verilog and Testbench generators
    without embedding HDL generation logic itself.
    """

    def __init__(self) -> None:
        self.verilog_generator = VerilogGenerator()
        self.testbench_generator = TestbenchGenerator()

    def generate(
        self,
        rtl_design: RTLDesign,
    ) -> tuple[str, str]:
        """
        Generate Verilog RTL and a Verilog testbench.

        Parameters
        ----------
        rtl_design:
            Structured RTL design.

        Returns
        -------
        tuple[str, str]
            (verilog_source, testbench_source)
        """

        verilog_source = self.verilog_generator.generate(
            rtl_design
        )

        testbench_source = self.testbench_generator.generate(
            rtl_design
        )

        return (
            verilog_source,
            testbench_source,
        )