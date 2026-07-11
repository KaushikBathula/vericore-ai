import logging

from backend.app.agents.base_agent import BaseAgent
from backend.app.ai.prompts import get_prompt
from backend.app.core.parsers.verification_parser import VerificationParser
from backend.app.schemas.verification_plan import VerificationPlan

logger = logging.getLogger(__name__)


class VerificationAgent(BaseAgent):
    """
    Converts RTL design requirements into a verification plan.
    """

    def __init__(self):
        super().__init__("VerificationAgent")

    def execute(self, rtl_design: str) -> VerificationPlan:
        """
        Generate verification strategy from RTL design.
        """

        logger.info("Starting verification planning.")

        system_prompt = get_prompt("verification")
        user_prompt = rtl_design

        response = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        if not response.success:
            raise RuntimeError(
                f"LLM generation failed: {response.error}"
            )

        plan = VerificationParser.parse(
            response.content
        )

        logger.info(
            "Verification planning completed successfully."
        )

        return plan