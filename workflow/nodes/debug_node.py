"""
LangGraph node for RTL debugging and repair.
"""

from __future__ import annotations

import logging

from backend.app.agents.debug_agent import DebugAgent
from backend.app.services.artifact_service import ArtifactService
from backend.app.services.code_generation_service import CodeGenerationService
from backend.app.services.rtl_repair_service import RTLRepairService
from workflow.state.design_state import DesignState


logger = logging.getLogger(__name__)


def debug_node(state: DesignState) -> dict:
    """
    Analyze a failed simulation and repair the RTL.

    Reads:
        state["simulation_result"]
        state["requirement_spec"]
        state["verification_plan"]
        state["project_paths"]

    Produces:
        repaired RTL/testbench artifacts and updated debug state.
    """

    logger.info("Starting Debug node.")

    simulation_result = state.get("simulation_result")
    requirement_spec = state.get("requirement_spec")
    verification_plan = state.get("verification_plan")
    project_paths = state.get("project_paths")

    if simulation_result is None:
        raise ValueError(
            "Simulation result is missing from workflow state."
        )

    if requirement_spec is None:
        raise ValueError(
            "Requirement specification is missing from workflow state."
        )

    if verification_plan is None:
        raise ValueError(
            "Verification plan is missing from workflow state."
        )

    if project_paths is None:
        raise ValueError(
            "Project paths are missing from workflow state."
        )

    # ---------------------------------------------------------
    # Analyze failure
    # ---------------------------------------------------------

    debug_agent = DebugAgent()

    debug_report = debug_agent.execute(
        simulation_result
    )

    # ---------------------------------------------------------
    # Repair RTL
    # ---------------------------------------------------------

    repair_service = RTLRepairService()

    rtl_design = repair_service.repair(
        requirement_spec=requirement_spec,
        debug_report=debug_report,
    )

    # ---------------------------------------------------------
    # Regenerate HDL
    # ---------------------------------------------------------

    code_generation_service = CodeGenerationService()

    rtl_source, testbench_source = (
        code_generation_service.generate(
            rtl_design=rtl_design,
            verification_plan=verification_plan,
        )
    )

    # ---------------------------------------------------------
    # Persist repaired artifacts
    # ---------------------------------------------------------

    artifact_service = ArtifactService()

    rtl_file = artifact_service.save_rtl(
        rtl_directory=project_paths["rtl"],
        module_name=requirement_spec.module_name,
        rtl_source=rtl_source,
    )

    testbench_file = artifact_service.save_testbench(
        testbench_directory=project_paths["testbench"],
        module_name=requirement_spec.module_name,
        testbench_source=testbench_source,
    )

    current_iteration = state.get(
        "debug_iteration",
        0,
    )

    new_iteration = current_iteration + 1

    logger.info(
        "RTL repair completed. Debug iteration=%d",
        new_iteration,
    )

    return {
        "debug_report": debug_report,
        "rtl_design": rtl_design,
        "rtl_source": rtl_source,
        "testbench_source": testbench_source,
        "rtl_file": rtl_file,
        "testbench_file": testbench_file,
        "debug_iteration": new_iteration,
        "current_stage": "debug_repair",
        "active_agent": "DebugAgent",
        "workflow_status": "rtl_repaired",
        "error": None,
    }