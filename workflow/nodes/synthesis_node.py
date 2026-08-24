"""
LangGraph node for RTL synthesis.
"""

from __future__ import annotations
import logging

from pathlib import Path

from backend.app.services.synthesis_service import SynthesisService
from workflow.state.design_state import DesignState


logger = logging.getLogger(__name__)


def synthesis_node(state: DesignState) -> dict:
    """
    Synthesize the generated RTL using Yosys.

    Reads:
        state["rtl_source"]
        state["requirement_spec"]
        state["project_paths"]

    Produces:
        state["synthesis_result"]
        state["netlist_file"]
    """

    logger.info("Starting Synthesis node.")

    rtl_source = state.get("rtl_source")
    requirement_spec = state.get("requirement_spec")
    project_paths = state.get("project_paths")

    if not rtl_source:
        raise ValueError(
            "RTL source is missing from workflow state."
        )

    if requirement_spec is None:
        raise ValueError(
            "Requirement specification is missing from workflow state."
        )

    if project_paths is None:
        raise ValueError(
            "Project paths are missing from workflow state."
        )

    synthesis_directory = project_paths.get(
        "synthesis"
    )

    if synthesis_directory is None:
        raise ValueError(
            "Synthesis directory is missing from project paths."
        )

    synthesis_service = SynthesisService()

    synthesis_result = synthesis_service.synthesize(
        rtl_source=rtl_source,
        top_module=requirement_spec.module_name,
        output_directory=synthesis_directory,
    )

    netlist_file = None

    if synthesis_result.netlist_path is not None:
        netlist_file = Path(synthesis_result.netlist_path)

    logger.info(
        "RTL synthesis completed. success=%s",
        synthesis_result.synthesis_success,
    )

    return {
        "synthesis_result": synthesis_result,
        "netlist_file": netlist_file,
        "current_stage": "synthesis",
        "active_agent": "SynthesisService",
        "workflow_status": (
            "synthesis_completed"
            if synthesis_result.synthesis_success
            else "synthesis_failed"
        ),
        "error": None,
    }

