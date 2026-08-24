"""
LangGraph node for documentation generation.
"""

from __future__ import annotations

import logging

from backend.app.schemas.documentation_report import DocumentationReport
from backend.app.services.documentation_service import DocumentationService
from workflow.state.design_state import DesignState


logger = logging.getLogger(__name__)


def documentation_node(state: DesignState) -> dict:
    """
    Build and save the final VeriCore AI documentation report.

    Reads the completed workflow state and produces:
        state["report"]
    """

    logger.info("Starting Documentation node.")

    requirement_text = state.get("requirement_text")
    requirement_spec = state.get("requirement_spec")
    rtl_design = state.get("rtl_design")
    verification_plan = state.get("verification_plan")
    rtl_source = state.get("rtl_source")
    testbench_source = state.get("testbench_source")
    simulation_result = state.get("simulation_result")
    synthesis_result = state.get("synthesis_result")
    post_synthesis_simulation_result = state.get(
        "post_synthesis_simulation_result"
    )
    debug_report = state.get("debug_report")
    project_paths = state.get("project_paths")

    if not requirement_text:
        raise ValueError(
            "Requirement text is missing from workflow state."
        )

    if requirement_spec is None:
        raise ValueError(
            "Requirement specification is missing from workflow state."
        )

    if rtl_design is None:
        raise ValueError(
            "RTL design is missing from workflow state."
        )

    if verification_plan is None:
        raise ValueError(
            "Verification plan is missing from workflow state."
        )

    if rtl_source is None:
        raise ValueError(
            "RTL source is missing from workflow state."
        )

    if testbench_source is None:
        raise ValueError(
            "Testbench source is missing from workflow state."
        )

    if project_paths is None:
        raise ValueError(
            "Project paths are missing from workflow state."
        )

    report = DocumentationReport(
        requirement_text=requirement_text,
        requirement_spec=requirement_spec,
        rtl_design=rtl_design,
        verification_plan=verification_plan,
        rtl_source=rtl_source,
        testbench_source=testbench_source,
        simulation_result=simulation_result,
        synthesis_result=synthesis_result,
        post_synthesis_simulation_result=(
            post_synthesis_simulation_result
        ),
        debug_report=debug_report,
        generated_files={},
        success=(
            simulation_result is not None
            and simulation_result.simulation_success
            and synthesis_result is not None
            and synthesis_result.synthesis_success
            and post_synthesis_simulation_result is not None
            and post_synthesis_simulation_result.simulation_success
        ),
    )

    documentation_service = DocumentationService()

    documentation_service.generate(
        report=report,
        output_directory=project_paths["documentation"],
    )

    logger.info(
        "Documentation generation completed."
    )

    return {
        "report": report,
        "current_stage": "documentation",
        "active_agent": "DocumentationService",
        "workflow_status": (
            "completed"
            if report.success
            else "completed_with_errors"
        ),
        "error": None,
    }