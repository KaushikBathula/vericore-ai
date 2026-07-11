from pydantic import BaseModel, Field

from backend.app.schemas.requirement_spec import RequirementSpec
from backend.app.schemas.rtl_design import RTLDesign


class GenerationRequest(BaseModel):
    """
    Request for the AI generation pipeline.
    """

    requirement: str = Field(
        ...,
        min_length=10,
        description="Natural language hardware requirement."
    )


class GenerationResponse(BaseModel):
    """
    Response returned by the AI generation pipeline.
    """

    requirement_spec: RequirementSpec

    rtl_design: RTLDesign