"""
RTL Repair Service.

Coordinates RTL regeneration after debug analysis.
"""

from __future__ import annotations

from backend.app.agents.rtl_agent import RTLAgent
from backend.app.schemas.debug_report import DebugReport
from backend.app.schemas.requirement_spec import RequirementSpec
from backend.app.schemas.rtl_design import RTLDesign


class RTLRepairService:
    """
    Coordinates automatic RTL repair.
    """

    def __init__(self) -> None:
        self.rtl_agent = RTLAgent()

    def repair(
        self,
        requirement_spec: RequirementSpec,
        debug_report: DebugReport,
    ) -> RTLDesign:
        """
        Regenerate RTL after analyzing debug results.

        Parameters
        ----------
        requirement_spec:
            Original hardware specification.

        debug_report:
            Debug analysis generated from the failed simulation.

        Returns
        -------
        RTLDesign
            Newly generated RTL design.
        """

        # Temporary implementation.
        # Later we'll pass debug information into the LLM prompt.
        return self.rtl_agent.execute(
            requirement=requirement_spec,
            debug_report=debug_report,
        )