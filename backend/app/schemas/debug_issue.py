"""
Debug Issue Schema.

Represents a single issue detected during RTL compilation
or simulation.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class DebugIssue(BaseModel):
    """
    Represents one debug issue identified by the Debug Agent.
    """

    category: str = Field(
        ...,
        description="Category of the issue.",
    )

    severity: str = Field(
        ...,
        description="Severity of the issue.",
    )

    message: str = Field(
        ...,
        description="Human-readable description of the issue.",
    )

    file: str | None = Field(
        default=None,
        description="Source file where the issue occurred.",
    )

    line: int | None = Field(
        default=None,
        ge=1,
        description="Source line number.",
    )

    suggestion: str = Field(
        default="",
        description="Suggested fix for the issue.",
    )