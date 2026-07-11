import logging

from app.agents.base_agent import BaseAgent
from app.ai.prompts import get_prompt
from app.core.parsers.response_parser import ResponseParser
from app.schemas.requirement_spec import RequirementSpec

logger = logging.getLogger(__name__)


class RequirementAgent(BaseAgent):
    """
    Converts natural language hardware requirements into
    a validated RequirementSpec using the configured LLM.
    """

    def __init__(self):
        super().__init__("RequirementAgent")

    def execute(self, requirement: str) -> RequirementSpec:
        """
        Generate a RequirementSpec from a natural language requirement.
        """

        logger.info("Starting requirement extraction.")

        system_prompt = get_prompt("requirements")
        user_prompt = requirement

        response = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        # Temporary debug output (remove after Feature 2 is complete)
        print("\n========== RAW LLM RESPONSE ==========\n")
        print(response.content)
        print("\n======================================\n")

        if not response.success:
            raise RuntimeError(
                f"LLM generation failed: {response.error}"
            )

        specification = ResponseParser.parse_requirement_response(
            response.content
        )

        logger.info("Requirement extraction completed successfully.")

        return specification