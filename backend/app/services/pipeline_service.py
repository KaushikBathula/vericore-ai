"""
Pipeline Service.

Entry point for executing the VeriCore AI LangGraph workflow.
"""

from __future__ import annotations

from pathlib import Path

from backend.app.agents.debug_agent import DebugAgent
from backend.app.agents.requirement_agent import RequirementAgent
from backend.app.agents.rtl_agent import RTLAgent
from backend.app.agents.verification_agent import VerificationAgent
from backend.app.services.artifact_service import ArtifactService
from backend.app.services.code_generation_service import CodeGenerationService
from backend.app.services.documentation_service import DocumentationService
from backend.app.services.rtl_repair_service import RTLRepairService
from backend.app.services.simulation_service import SimulationService
from backend.app.services.synthesis_service import SynthesisService
from backend.app.schemas.documentation_report import DocumentationReport

from workflow.graph import design_graph


class PipelineService:
    """
    Coordinates the VeriCore AI workflow through LangGraph.

    Legacy service attributes are retained for compatibility with
    existing tests and integrations.
    """

    def __init__(self) -> None:
        # Keep these attributes for backward compatibility.
        self.requirement_agent = RequirementAgent()
        self.rtl_agent = RTLAgent()
        self.verification_agent = VerificationAgent()

        self.artifact_service = ArtifactService()
        self.code_generation_service = CodeGenerationService()
        self.simulation_service = SimulationService()
        self.synthesis_service = SynthesisService()
        self.documentation_service = DocumentationService()

        self.rtl_repair_service = RTLRepairService()
        self.debug_agent = DebugAgent()

        self.max_debug_iterations = 3

    def execute(
        self,
        requirement_text: str,
        output_directory: Path,
    ) -> DocumentationReport:
        """
        Execute the complete VeriCore AI workflow through LangGraph.
        """

        if not requirement_text:
            raise ValueError(
                "Requirement text cannot be empty."
            )

        print("\n########################################")
        print("### LANGGRAPH PIPELINE IS RUNNING ###")
        print("########################################\n")

        initial_state = {
            "requirement_text": requirement_text,
            "output_directory": output_directory,
            "debug_iteration": 0,
            "max_debug_iterations": self.max_debug_iterations,
            "current_stage": "starting",
            "active_agent": "LangGraph",
            "workflow_status": "starting",
            "error": None,
        }

        result = design_graph.invoke(
            initial_state
        )

        report = result.get("report")

        if report is None:
            raise RuntimeError(
                "LangGraph completed without producing "
                "a documentation report."
            )

        print("\n########################################")
        print("### LANGGRAPH PIPELINE COMPLETED ###")
        print("########################################\n")

        return report