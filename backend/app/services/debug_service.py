"""
Debug Service.

Coordinates debug analysis of simulation results.
"""

from __future__ import annotations

from backend.app.agents.debug_agent import DebugAgent
from backend.app.schemas.debug_report import DebugReport
from backend.app.schemas.simulation_result import SimulationResult


class DebugService:
    """
    Coordinates debug analysis.
    """

    def __init__(self) -> None:
        self.debug_agent = DebugAgent()

    def analyze(
        self,
        simulation_result: SimulationResult,
    ) -> DebugReport:
        """
        Analyze a simulation result.

        Parameters
        ----------
        simulation_result:
            Result produced by the simulation pipeline.

        Returns
        -------
        DebugReport
            Structured debug report.
        """

        return self.debug_agent.execute(
            simulation_result,
        )