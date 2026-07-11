from typing import Any

from pydantic import BaseModel, Field

from app.schemas.operation import Operation
from app.schemas.port import Port
from app.schemas.verification_point import VerificationPoint


class RequirementSpec(BaseModel):
    """
    Structured engineering specification generated
    from natural language hardware requirements.
    """

    module_name: str

    description: str

    inputs: list[Port] = Field(default_factory=list)

    outputs: list[Port] = Field(default_factory=list)

    operations: list[Operation] = Field(default_factory=list)

    parameters: dict[str, Any] = Field(default_factory=dict)

    verification_points: list[VerificationPoint] = Field(default_factory=list)