from pydantic import BaseModel, Field


class VerificationPoint(BaseModel):
    """
    Represents an important verification scenario.
    """

    description: str = Field(
        ...,
        description="Verification objective."
    )

    test_case: str | None = Field(
        default=None,
        description="Example verification test."
    )

    point_name: str | None = Field(
        default=None,
        description="Optional verification point name."
    )