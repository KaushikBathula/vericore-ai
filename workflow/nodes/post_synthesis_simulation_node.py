"""
LangGraph node for post-synthesis simulation.
"""

from __future__ import annotations

import logging

from backend.app.services.simulation_service import SimulationService
from workflow.state.design_state import DesignState


logger = logging.getLogger(__name__)


def post_synthesis_simulation_node(state: DesignState) -> dict:
    """
    Simulate the synthesized netlist using the existing testbench.

    Reads:
        state["netlist_file"]
        state["testbench_file"]
        state["project_paths"]

    Produces:
        state["post_synthesis_simulation_result"]
    """

    logger.info(
        "Starting post-synthesis simulation node."
    )

    netlist_file = state.get("netlist_file")
    testbench_file = state.get("testbench_file")
    project_paths = state.get("project_paths")

    if netlist_file is None:
        raise ValueError(
            "Synthesized netlist is missing from workflow state."
        )

    if testbench_file is None:
        raise ValueError(
            "Testbench file is missing from workflow state."
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

    simulation_service = SimulationService()

    result = simulation_service.simulate(
        rtl_file=netlist_file,
        testbench_file=testbench_file,
        working_directory=synthesis_directory,
    )

    logger.info(
        "Post-synthesis simulation completed. success=%s",
        result.simulation_success,
    )

    return {
        "post_synthesis_simulation_result": result,
        "current_stage": "post_synthesis_simulation",
        "active_agent": "SimulationService",
        "workflow_status": (
            "post_synthesis_simulation_completed"
            if result.simulation_success
            else "post_synthesis_simulation_failed"
        ),
        "error": None,
    }