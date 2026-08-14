"""
Synthesis Service.

Coordinates RTL synthesis using Yosys.
"""

from __future__ import annotations

from pathlib import Path

from backend.app.schemas.synthesis_result import SynthesisResult
from backend.app.synthesis.synthesis_runner import SynthesisRunner
from backend.app.synthesis.yosys_script_generator import (
    YosysScriptGenerator,
)


class SynthesisService:
    """
    Coordinates RTL synthesis.

    This service manages synthesis artifacts and delegates
    synthesis execution to the SynthesisRunner.
    """

    def __init__(self) -> None:
        self.runner = SynthesisRunner()
        self.script_generator = YosysScriptGenerator()

    def synthesize(
        self,
        rtl_source: str,
        top_module: str,
        output_directory: Path,
    ) -> SynthesisResult:
        """
        Synthesize generated RTL.

        Parameters
        ----------
        rtl_source:
            Verilog RTL source code.

        top_module:
            Top-level module name.

        output_directory:
            Directory where synthesis artifacts are stored.

        Returns
        -------
        SynthesisResult
            Result of RTL synthesis.
        """

        output_directory = output_directory.resolve()

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        rtl_file = output_directory / "design.v"
        yosys_script = output_directory / "design.ys"
        netlist_file = output_directory / "netlist.v"
        report_file = output_directory / "yosys.log"

        rtl_file.write_text(
            rtl_source,
            encoding="utf-8",
        )

        script = self.script_generator.generate(
            rtl_file=rtl_file,
            top_module=top_module,
            netlist_file=netlist_file,
        )

        yosys_script.write_text(
            script,
            encoding="utf-8",
        )

        return self.runner.run(
            rtl_file=rtl_file,
            yosys_script=yosys_script,
            netlist_file=netlist_file,
            report_file=report_file,
        )
