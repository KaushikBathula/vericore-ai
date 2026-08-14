"""
Schema representing the result of RTL synthesis.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class SynthesisResult(BaseModel):
    """
    Represents the outcome of synthesizing an RTL design.
    """

    synthesis_success: bool = Field(
        ...,
        description="Whether synthesis completed successfully.",
    )

    stdout: str = Field(
        default="",
        description="Standard output produced by the synthesis tool.",
    )

    stderr: str = Field(
        default="",
        description="Standard error produced by the synthesis tool.",
    )

    execution_time: float = Field(
        default=0.0,
        ge=0.0,
        description="Synthesis execution time in seconds.",
    )

    netlist_path: str | None = Field(
        default=None,
        description="Path to the generated synthesized netlist.",
    )

    report_path: str | None = Field(
        default=None,
        description="Path to the synthesis report.",
    )

    cell_count: int | None = Field(
        default=None,
        ge=0,
        description="Total number of synthesized cells.",
    )

    warning_count: int = Field(
        default=0,
        ge=0,
        description="Number of synthesis warnings.",
    )

    synthesis_output: str = Field(
        default="",
        description="Complete synthesis tool output.",
    )