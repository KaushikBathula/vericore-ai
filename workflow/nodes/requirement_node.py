"""
LangGraph node for requirement analysis.
"""

from __future__ import annotations

import logging

from backend.app.agents.requirement_agent import RequirementAgent
from backend.app.services.artifact_service import ArtifactService
from workflow.state.design_state import DesignState


logger = logging.getLogger(__name__)


def requirement_node(state: DesignState) -> dict:
    """
    Analyze the natural-language hardware requirement.

    Produces:
        requirement_spec
        project_paths
    """

    logger.info("Starting Requirement node.")

    requirement_text = state.get("requirement_text")

    if not requirement_text:
        raise ValueError(
            "Requirement text is missing from workflow state."
        )

    agent = RequirementAgent()

    requirement_spec = agent.execute(
        requirement_text
    )

    artifact_service = ArtifactService()

    project_paths = artifact_service.create_project(
        requirement_spec.module_name
    )

    logger.info(
        "Requirement analysis completed for module '%s'.",
        requirement_spec.module_name,
    )

    return {
        "requirement_spec": requirement_spec,
        "project_paths": project_paths,
        "current_stage": "requirement_analysis",
        "active_agent": "RequirementAgent",
        "workflow_status": "requirement_completed",
        "error": None,
    }