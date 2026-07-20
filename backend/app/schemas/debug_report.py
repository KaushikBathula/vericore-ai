"""
Debug Report Schema.

Represents the complete result of a compilation or
simulation debugging session.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from backend.app.schemas.debug_issue import DebugIssue


class DebugReport(BaseModel):
    """
    Represents the overall debugging report.
    """

    success: bool = Field(
        ...,
        description="Whether compilation/simulation succeeded.",
    )

    summary: str = Field(
        default="",
        description="High-level summary of the debug session.",
    )

    issues: list[DebugIssue] = Field(
        default_factory=list,
        description="Detected issues.",
    )

    compiler_output: str = Field(
        default="",
        description="Compiler diagnostics.",
    )

    simulation_output: str = Field(
        default="",
        description="Simulation diagnostics.",
    )

    recommendations: list[str] = Field(
        default_factory=list,
        description="Recommended actions.",
    )