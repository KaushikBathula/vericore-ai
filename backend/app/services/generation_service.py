from backend.app.agents.requirement_agent import RequirementAgent
from backend.app.agents.rtl_agent import RTLAgent
from backend.app.schemas.requirement_spec import RequirementSpec
from backend.app.schemas.rtl_design import RTLDesign


class GenerationService:
    """
    Coordinates the AI generation pipeline.
    """

    def __init__(self):
        self.requirement_agent = RequirementAgent()
        self.rtl_agent = RTLAgent()

    def generate(
        self,
        requirement: str,
    ) -> tuple[RequirementSpec, RTLDesign]:
        """
        Execute the complete AI pipeline.

        Natural Language
            ↓
        RequirementSpec
            ↓
        RTLDesign
        """

        requirement_spec = self.requirement_agent.execute(
            requirement
        )

        rtl_design = self.rtl_agent.execute(
            requirement_spec
        )

        return requirement_spec, rtl_design