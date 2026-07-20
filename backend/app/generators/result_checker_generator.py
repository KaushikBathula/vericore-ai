"""
Result Checker Generator

Generates self-checking Verilog statements for expected DUT outputs.
"""

from __future__ import annotations

from backend.app.generators.base_generator import BaseGenerator
from backend.app.schemas.test_vector import TestVector


class ResultCheckerGenerator(BaseGenerator):
    """
    Generates Verilog output checking logic.
    """

    def generate(
        self,
        test_vector: TestVector,
    ) -> list[str]:

        lines: list[str] = []

        if not test_vector.expected_outputs:
            return lines

        lines.append("    // Check DUT outputs")

        for signal, expected in test_vector.expected_outputs.items():

            if isinstance(expected, str):
                expected = f'"{expected}"'

            lines.extend(
                [
                    f"    if ({signal} !== {expected}) begin",
                    f'        $display("FAIL: {signal} expected={expected}, got=%0d", {signal});',
                    "        $fatal;",
                    "    end",
                    "",
                ]
            )

        return lines