from typing import Any

from pydantic import BaseModel, Field

from backend.app.schemas.operation import Operation
from backend.app.schemas.requirement_spec import RequirementSpec
from backend.app.schemas.signal import Signal


class RTLDesign(BaseModel):
    """
    Represents the AI-generated RTL implementation derived
    from a validated RequirementSpec.
    """

    requirement: RequirementSpec = Field(
        ...,
        description="Original validated hardware requirement."
    )

    internal_signals: list[Signal] = Field(
        default_factory=list,
        description="Internal RTL signals."
    )

    implementation_strategy: str = Field(
        default="",
        description="Implementation strategy."
    )

    derived_operations: list[Operation] = Field(
        default_factory=list,
        description="RTL operations."
    )

    # NEW
    parameters: dict[str, int | str] = Field(
        default_factory=dict,
        description="Module parameters."
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata."
    )