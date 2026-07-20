"""
Waveform Generator

Generates waveform dump logic for Verilog testbenches.
"""

from __future__ import annotations

from backend.app.generators.base_generator import BaseGenerator


class WaveformGenerator(BaseGenerator):
    """
    Generates VCD waveform dump logic.
    """

    def generate(
        self,
        testbench_name: str,
    ) -> list[str]:
        """
        Generate waveform dump statements.

        Parameters
        ----------
        testbench_name:
            Name of the generated testbench module.

        Returns
        -------
        list[str]
            Verilog source lines.
        """

        lines: list[str] = []

        lines.append("initial begin")
        lines.append(
            f'    $dumpfile("{testbench_name}.vcd");'
        )
        lines.append(
            f"    $dumpvars(0, {testbench_name});"
        )
        lines.append("end")

        self.add_blank_line(lines)

        return lines