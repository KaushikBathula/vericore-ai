"""
Debug Agent.

Analyzes simulation results and produces a structured
DebugReport.
"""

from __future__ import annotations

import logging

from backend.app.agents.base_agent import BaseAgent
from backend.app.core.parsers.debug_parser import DebugParser
from backend.app.schemas.debug_report import DebugReport
from backend.app.schemas.simulation_result import SimulationResult

logger = logging.getLogger(__name__)


class DebugAgent(BaseAgent):
    """
    Analyzes compiler and simulator output.
    """

    def __init__(self) -> None:
        super().__init__("DebugAgent")

    def execute(
        self,
        simulation_result: SimulationResult,
    ) -> DebugReport:
        """
        Analyze a simulation result.

        Parameters
        ----------
        simulation_result:
            Result returned by the simulation pipeline.

        Returns
        -------
        DebugReport
            Structured debugging report.
        """

        logger.info("Starting debug analysis.")

        report = DebugParser.parse(
            compiler_output=simulation_result.compiler_output,
            simulation_output=simulation_result.simulation_output,
        )

        logger.info("Debug analysis completed.")

        return report