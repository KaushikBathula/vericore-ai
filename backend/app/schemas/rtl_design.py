from typing import Any

from pydantic import BaseModel, Field

from backend.app.schemas.operation import Operation
from backend.app.schemas.requirement_spec import RequirementSpec
from backend.app.schemas.signal import Signal


class RTLDesign(BaseModel):
    """
    Represents the AI-generated RTL implementation derived
    from a validated RequirementSpec.

    This model serves as the canonical implementation model
    for all downstream generators such as Verilog,
    testbench, assertions, documentation, and synthesis.
    """

    requirement: RequirementSpec = Field(
        ...,
        description="Original validated hardware requirement."
    )

    internal_signals: list[Signal] = Field(
        default_factory=list,
        description="Internal RTL signals required for implementation."
    )

    implementation_strategy: str = Field(
        default="",
        description="High-level implementation approach chosen by the AI."
    )

    derived_operations: list[Operation] = Field(
        default_factory=list,
        description="Operations after RTL refinement."
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional implementation metadata."
    )