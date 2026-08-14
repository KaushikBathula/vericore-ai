import logging

from backend.app.agents.base_agent import BaseAgent
from backend.app.ai.prompts import get_prompt
from backend.app.core.parsers import RTLResponseParser
from backend.app.schemas.requirement_spec import RequirementSpec
from backend.app.schemas.rtl_design import RTLDesign
from backend.app.schemas.debug_report import DebugReport

logger = logging.getLogger(__name__)


class RTLAgent(BaseAgent):
    """
    Generates an RTL implementation plan from a RequirementSpec.
    """

    def __init__(self):
        super().__init__("RTLAgent")

    def execute(
        self,
        requirement: RequirementSpec,
        debug_report: DebugReport | None = None,
    ) -> RTLDesign:

        logger.info("Starting RTL generation.")

        system_prompt = get_prompt("rtl")

        user_prompt = requirement.model_dump_json(
            indent=2,
        )

        if debug_report is not None:

            user_prompt += (
                "\n\n"
                "Previous RTL implementation failed.\n\n"
                "Debug Report:\n"
                f"{debug_report.model_dump_json(indent=2)}\n\n"
                "Revise the RTL to fix all reported issues "
                "while preserving the original functionality."
            )

        response = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        if not response.success:
            raise RuntimeError(
                f"LLM generation failed: {response.error}"
            )

        # -----------------------------------------------------
        # RAW LLM OUTPUT
        # -----------------------------------------------------

        print("\n========== RAW RTL RESPONSE ==========\n")
        print(response.content)
        print("\n======================================\n")

        rtl_design = RTLResponseParser.parse(
            response.content,
            requirement,
        )

        # -----------------------------------------------------
        # PARSED RTL DESIGN
        # -----------------------------------------------------

        print("\n========== PARSED RTL DESIGN ==========\n")
        print(rtl_design.model_dump())
        print("\n=======================================\n")

        logger.info("RTL generation completed successfully.")

        return rtl_design