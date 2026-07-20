"""
Simulation Service.

Coordinates RTL simulation using the SimulationRunner.
"""

from __future__ import annotations

from pathlib import Path

from backend.app.schemas.simulation_result import SimulationResult
from backend.app.services.simulation_runner import SimulationRunner


class SimulationService:
    """
    Coordinates RTL simulation.

    This service orchestrates the simulation workflow without
    embedding simulator-specific logic.
    """

    def __init__(self) -> None:
        self.simulation_runner = SimulationRunner()

    def simulate(
        self,
        rtl_file: Path,
        testbench_file: Path,
        working_directory: Path,
    ) -> SimulationResult:
        """
        Compile and simulate RTL.

        Parameters
        ----------
        rtl_file:
            Path to the generated RTL file.

        testbench_file:
            Path to the generated testbench.

        working_directory:
            Directory used for simulation artifacts.

        Returns
        -------
        SimulationResult
            Result of compilation and simulation.
        """

        working_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_file = working_directory / "simulation.out"

        return self.simulation_runner.run(
            rtl_file=rtl_file,
            testbench_file=testbench_file,
            output_file=output_file,
            working_directory=working_directory,
        )