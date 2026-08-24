"""
LangGraph node for verification planning and HDL generation.
"""

from __future__ import annotations

import logging

from backend.app.agents.verification_agent import VerificationAgent
from backend.app.services.artifact_service import ArtifactService
from backend.app.services.code_generation_service import (
    CodeGenerationService,
)
from workflow.state.design_state import DesignState


logger = logging.getLogger(__name__)


def verification_node(state: DesignState) -> dict:
    """
    Generate the verification plan and materialize HDL artifacts.

    Reads:
        state["requirement_spec"]
        state["rtl_design"]
        state["project_paths"]

    Produces:
        state["verification_plan"]
        state["rtl_source"]
        state["testbench_source"]
        state["rtl_file"]
        state["testbench_file"]
    """

    logger.info("Starting Verification node.")

    requirement_spec = state.get("requirement_spec")
    rtl_design = state.get("rtl_design")
    project_paths = state.get("project_paths")

    if requirement_spec is None:
        raise ValueError(
            "Requirement specification is missing from workflow state."
        )

    if rtl_design is None:
        raise ValueError(
            "RTL design is missing from workflow state."
        )

    if project_paths is None:
        raise ValueError(
            "Project paths are missing from workflow state."
        )

    verification_agent = VerificationAgent()

    verification_plan = verification_agent.execute(
        requirement_spec=requirement_spec,
        rtl_design=rtl_design,
    )

    code_generation_service = CodeGenerationService()

    rtl_source, testbench_source = (
        code_generation_service.generate(
            rtl_design=rtl_design,
            verification_plan=verification_plan,
        )
    )

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

    logger.info(
        "Verification planning and HDL generation completed."
    )

    return {
        "verification_plan": verification_plan,
        "rtl_source": rtl_source,
        "testbench_source": testbench_source,
        "rtl_file": rtl_file,
        "testbench_file": testbench_file,
        "current_stage": "verification_planning",
        "active_agent": "VerificationAgent",
        "workflow_status": "verification_completed",
        "error": None,
    }