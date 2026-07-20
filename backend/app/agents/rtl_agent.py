import logging

from backend.app.agents.base_agent import BaseAgent
from backend.app.ai.prompts import get_prompt
from backend.app.core.parsers import RTLResponseParser
from backend.app.schemas.requirement_spec import RequirementSpec
from backend.app.schemas.rtl_design import RTLDesign

logger = logging.getLogger(__name__)


class RTLAgent(BaseAgent):
    """
    Generates an RTL implementation plan from a RequirementSpec.
    """

    def __init__(self):
        super().__init__("RTLAgent")

    def execute(self, requirement: RequirementSpec) -> RTLDesign:

        logger.info("Starting RTL generation.")

        system_prompt = get_prompt("rtl")
        user_prompt = requirement.model_dump_json(indent=2)

        response = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        if not response.success:
            raise RuntimeError(
                f"LLM generation failed: {response.error}"
            )

        # -----------------------------------------------------
        # Temporary debug output
        # Remove after parser issue is resolved
        # -----------------------------------------------------
        

        rtl_design = RTLResponseParser.parse(
            response.content,
            requirement,
        )

        logger.info("RTL generation completed successfully.")

        return rtl_design