import json

from pydantic import ValidationError

from backend.app.schemas.requirement_spec import RequirementSpec
from backend.app.schemas.rtl_design import RTLDesign


class RTLResponseParser:
    """
    Converts raw LLM responses into validated RTLDesign objects.
    """

    @staticmethod
    def parse(
        response: str,
        requirement: RequirementSpec,
    ) -> RTLDesign:

        data = json.loads(response)

        data["requirement"] = requirement

        try:
            return RTLDesign.model_validate(data)

        except ValidationError as exc:
            raise ValueError(
                f"RTL design validation failed:\n{exc}"
            ) from exc