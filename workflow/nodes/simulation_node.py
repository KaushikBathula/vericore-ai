"""
LangGraph node for RTL simulation.
"""

from __future__ import annotations

import logging

from backend.app.services.simulation_service import SimulationService
from workflow.state.design_state import DesignState


logger = logging.getLogger(__name__)


def simulation_node(state: DesignState) -> dict:
    """
    Run RTL simulation.

    Reads:
        state["rtl_file"]
        state["testbench_file"]
        state["project_paths"]

    Produces:
        state["simulation_result"]
    """

    logger.info("Starting Simulation node.")

    rtl_file = state.get("rtl_file")
    testbench_file = state.get("testbench_file")
    project_paths = state.get("project_paths")

    if rtl_file is None:
        raise ValueError(
            "RTL file is missing from workflow state."
        )

    if testbench_file is None:
        raise ValueError(
            "Testbench file is missing from workflow state."
        )

    if project_paths is None:
        raise ValueError(
            "Project paths are missing from workflow state."
        )

    simulation_directory = project_paths.get(
        "simulation"
    )

    if simulation_directory is None:
        raise ValueError(
            "Simulation directory is missing from project paths."
        )

    simulation_service = SimulationService()

    simulation_result = simulation_service.simulate(
        rtl_file=rtl_file,
        testbench_file=testbench_file,
        working_directory=simulation_directory,
    )

    logger.info(
        "RTL simulation completed. success=%s",
        simulation_result.simulation_success,
    )

    return {
        "simulation_result": simulation_result,
        "current_stage": "simulation",
        "active_agent": "SimulationService",
        "workflow_status": (
            "simulation_completed"
            if simulation_result.simulation_success
            else "simulation_failed"
        ),
        "error": None,
    }