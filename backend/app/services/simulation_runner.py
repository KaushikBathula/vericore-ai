"""
Simulation Runner.

Executes RTL compilation and simulation using Icarus Verilog.
"""

from __future__ import annotations

import subprocess
import time
from pathlib import Path

from backend.app.core.logging import get_logger
from backend.app.schemas.simulation_result import SimulationResult

logger = get_logger(__name__)


class SimulationRunner:
    """
    Executes RTL compilation and simulation.

    This class is responsible only for interacting with the simulator.
    It does not create files or manage project directories.
    """

    def run(
        self,
        rtl_file: Path,
        testbench_file: Path,
        output_file: Path,
        working_directory: Path,
    ) -> SimulationResult:
        """
        Compile and simulate an RTL design.

        Parameters
        ----------
        rtl_file:
            Path to the Verilog RTL source.

        testbench_file:
            Path to the generated testbench.

        output_file:
            Path of the compiled simulation executable.

        Returns
        -------
        SimulationResult
            Result of compilation and simulation.
        """

        if not rtl_file.exists():
            raise FileNotFoundError(f"RTL file not found: {rtl_file}")

        if not testbench_file.exists():
            raise FileNotFoundError(
                f"Testbench file not found: {testbench_file}"
            )

        compile_command = [
            "iverilog",
            "-o",
            str(output_file),
            str(rtl_file),
            str(testbench_file),
        ]

        logger.info("Compiling RTL using Icarus Verilog.")

        start_time = time.perf_counter()

        compile_process = subprocess.run(
            compile_command,
            capture_output=True,
            text=True,
        )

        if compile_process.returncode != 0:
            elapsed = time.perf_counter() - start_time

            logger.error("Compilation failed.")

            return SimulationResult(
                compile_success=False,
                simulation_success=False,
                stdout="",
                stderr=compile_process.stderr,
                execution_time=elapsed,
                waveform_path=None,
                compiler_output=compile_process.stdout
                + compile_process.stderr,
                simulation_output="",
            )

        logger.info("Compilation successful. Starting simulation.")

        simulation_process = subprocess.run(
            [
                "vvp",
                str(output_file),
            ],
            capture_output=True,
            text=True,
        )

        elapsed = time.perf_counter() - start_time

        simulation_success = simulation_process.returncode == 0
        waveform_files = sorted(
            working_directory.glob("*.vcd")
        )

        waveform_path = (
            str(waveform_files[0])
            if waveform_files
            else None
        )

        if simulation_success:
            logger.info("Simulation completed successfully.")
        else:
            logger.error("Simulation failed.")

        return SimulationResult(
            compile_success=True,
            simulation_success=simulation_success,
            stdout=simulation_process.stdout,
            stderr=simulation_process.stderr,
            execution_time=elapsed,
            waveform_path=waveform_path,
            compiler_output=compile_process.stdout
            + compile_process.stderr,
            simulation_output=simulation_process.stdout
            + simulation_process.stderr,
        )