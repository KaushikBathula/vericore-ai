from backend.app.agents.requirement_agent import RequirementAgent
from backend.app.agents.rtl_agent import RTLAgent
from backend.app.agents.verification_agent import VerificationAgent

from backend.app.schemas.requirement_spec import RequirementSpec
from backend.app.schemas.rtl_design import RTLDesign
from backend.app.schemas.verification_plan import VerificationPlan


class GenerationService:
    """
    Coordinates the AI generation pipeline.
    """

    def __init__(self):
        self.requirement_agent = RequirementAgent()
        self.rtl_agent = RTLAgent()
        self.verification_agent = VerificationAgent()

    def generate(
        self,
        requirement: str,
    ) -> tuple[
        RequirementSpec,
        RTLDesign,
        VerificationPlan,
    ]:
        """
        Execute complete AI pipeline.

        Requirement
            ↓
        RequirementSpec
            ↓
        RTLDesign
            ↓
        VerificationPlan
        """

        requirement_spec = self.requirement_agent.execute(
            requirement
        )

        rtl_design = self.rtl_agent.execute(
            requirement_spec
        )

        verification_plan = self.verification_agent.execute(
            requirement_spec,
            rtl_design,
        )

        return (
            requirement_spec,
            rtl_design,
            verification_plan,
        )
