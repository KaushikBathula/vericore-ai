"""
LangGraph node for RTL design generation.
"""

from __future__ import annotations

import logging

from backend.app.agents.rtl_agent import RTLAgent
from workflow.state.design_state import DesignState


logger = logging.getLogger(__name__)


def rtl_node(state: DesignState) -> dict:
    """
    Generate the RTL design.

    Reads:
        state["requirement_spec"]

    Produces:
        state["rtl_design"]
    """

    logger.info("Starting RTL node.")

    requirement_spec = state.get("requirement_spec")

    if requirement_spec is None:
        raise ValueError(
            "Requirement specification is missing from workflow state."
        )

    rtl_agent = RTLAgent()

    rtl_design = rtl_agent.execute(
        requirement_spec
    )

    logger.info(
        "RTL design generation completed for module '%s'.",
        requirement_spec.module_name,
    )

    return {
        "rtl_design": rtl_design,
        "current_stage": "rtl_generation",
        "active_agent": "RTLAgent",
        "workflow_status": "rtl_completed",
        "error": None,
    }