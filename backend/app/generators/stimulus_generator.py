"""
Stimulus Generator

Generates the initial stimulus block for a Verilog
testbench.
"""

from __future__ import annotations
from backend.app.generators.result_checker_generator import ResultCheckerGenerator
from backend.app.generators.base_generator import BaseGenerator
from backend.app.generators.constants import CLOCK_SIGNAL_NAMES
from backend.app.schemas.requirement_spec import RequirementSpec


RESET_SIGNAL_NAMES = {
    "rst",
    "reset",
    "rst_n",
    "reset_n",
}


class StimulusGenerator(BaseGenerator):
    """
    Generates stimulus for the DUT.
    """
    def __init__(self):
        self.result_checker = ResultCheckerGenerator()
    def generate(
        self,
        requirement: RequirementSpec,
        verification_plan=None,
    ) -> list[str]:
        """
        Generate a stimulus block.

        If an AI-generated VerificationPlan is available,
        generate stimulus from its test vectors.
        Otherwise, fall back to default initialization.
        """

        lines: list[str] = []

        lines.append("initial begin")

        # ----------------------------------------
        # Initialize all non-clock/non-reset inputs
        # ----------------------------------------

        for port in requirement.inputs:

            signal_name = port.signal_name.lower()

            if signal_name in CLOCK_SIGNAL_NAMES:
                continue

            if signal_name in RESET_SIGNAL_NAMES:
                continue

            lines.append(f"    {port.signal_name} = 0;")

        lines.append("")
        lines.append("    #20;")
        lines.append("")

        # ----------------------------------------
        # AI Generated Test Vectors
        # ----------------------------------------

        if (
            verification_plan is not None
            and verification_plan.test_vectors
        ):

            lines.append("    // AI Generated Test Vectors")
            lines.append("")
            print("\n========== TEST VECTORS ==========")
            for i, vector in enumerate(verification_plan.test_vectors, start=1):
                print(f"Vector {i}")
                print(vector.model_dump())
            print("==================================\n")
                

            for vector in verification_plan.test_vectors:

                lines.append(f"    // {vector.name}")

                for signal, value in vector.inputs.items():

                    if isinstance(value, str):
                        value = f'"{value}"'

                    lines.append(f"    {signal} = {value};")

                lines.append(f"    #{vector.delay};")
                lines.extend(
                    self.result_checker.generate(vector)
                )

                lines.append("")

        else:

            lines.append(
                "    // TODO: Automatic stimulus generation"
            )
            lines.append("")

        lines.append("    $finish;")
        lines.append("end")

        self.add_blank_line(lines)

        return lines