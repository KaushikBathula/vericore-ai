"""
Verification Point Schema.

Represents a single verification objective for a hardware design.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict


class VerificationPoint(BaseModel):
    """
    Represents a verification point generated from a hardware requirement.
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )

    description: str = Field(
        default="",
        description="Description of what should be verified.",
    )

    test_case: str | None = Field(
        default=None,
        description="Optional test case associated with this verification point.",
    )

    point_name: str | None = Field(
        default=None,
        alias="name",
        description="Name of the verification point.",
    )

    @property
    def name(self) -> str | None:
        """
        Backward-compatible access to the verification point name.

        Internally the schema uses `point_name`, while callers and
        older tests may use `name`.
        """
        return self.point_name