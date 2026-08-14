"""
Synthesis Runner.

Executes RTL synthesis using Yosys.
"""

from __future__ import annotations

import subprocess
import time
import os
from pathlib import Path

from backend.app.core.logging import get_logger
from backend.app.core.toolchain import resolve_executable
from backend.app.schemas.synthesis_result import SynthesisResult
from backend.app.synthesis.yosys_report_parser import (
    YosysReportParser,
)

logger = get_logger(__name__)


class SynthesisRunner:
    """
    Executes RTL synthesis using Yosys.

    This class is responsible only for invoking the synthesis tool.
    It does not create directories or manage project files.
    """

    def _build_yosys_environment(self, yosys: str) -> dict[str, str]:
        """
        Build an execution environment for Yosys.

        OSS CAD Suite on Windows needs both `bin` and `lib` on PATH.
        Without that, `yosys.exe` can exit with Windows loader code
        -1073741515 before producing stdout or stderr.
        """

        env = os.environ.copy()
        yosys_path = Path(yosys)
        suite_root = yosys_path.parent.parent
        suite_lib = suite_root / "lib"

        if suite_lib.exists():
            existing_path = env.get("PATH", "")
            env["YOSYSHQ_ROOT"] = str(suite_root)
            env["PATH"] = (
                f"{yosys_path.parent}{os.pathsep}"
                f"{suite_lib}{os.pathsep}"
                f"{existing_path}"
            )

        return env

    def run(
        self,
        rtl_file: Path,
        yosys_script: Path,
        netlist_file: Path,
        report_file: Path,
    ) -> SynthesisResult:
        """
        Run RTL synthesis.

        Parameters
        ----------
        rtl_file:
            Path to the RTL Verilog file.

        yosys_script:
            Path to the generated Yosys script.

        netlist_file:
            Expected output netlist path.

        report_file:
            Expected synthesis report path.

        Returns
        -------
        SynthesisResult
            Result of the synthesis process.
        """

        if not rtl_file.exists():
            raise FileNotFoundError(
                f"RTL file not found: {rtl_file}"
            )

        if not yosys_script.exists():
            raise FileNotFoundError(
                f"Yosys script not found: {yosys_script}"
            )

        yosys = resolve_executable(
            tool_name="yosys",
            stage="Synthesis",
        )

        command = [
            yosys,
            "-s",
            str(yosys_script.resolve()),
        ]

        logger.info("Starting RTL synthesis using Yosys.")

        start_time = time.perf_counter()

        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=report_file.parent,
            env=self._build_yosys_environment(yosys),
        )

        elapsed = time.perf_counter() - start_time

        synthesis_success = process.returncode == 0

        if synthesis_success:
            logger.info("Synthesis completed successfully.")
        else:
            logger.error("Synthesis failed.")

        combined_output = (
            process.stdout
            + process.stderr
        )

        report_file.write_text(
            combined_output,
            encoding="utf-8",
        )

        warning_count = YosysReportParser.parse_warning_count(
            combined_output
        )

        cell_count = YosysReportParser.parse_cell_count(
            combined_output
        )

        return SynthesisResult(
            synthesis_success=synthesis_success,
            stdout=process.stdout,
            stderr=process.stderr,
            execution_time=elapsed,
            netlist_path=(
                str(netlist_file)
                if netlist_file.exists()
                else None
            ),
            report_path=(
                str(report_file)
                if report_file.exists()
                else None
            ),
            cell_count=cell_count,
            warning_count=warning_count,
            synthesis_output=combined_output,
        )
