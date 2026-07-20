"""
Test Vector Schema

Represents a single verification scenario for the DUT.
Each test vector defines the applied inputs and the
expected DUT outputs.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class TestVector(BaseModel):
    """
    Represents one verification test vector.
    """

    name: str = Field(
        ...,
        description="Unique name of the test vector.",
    )

    description: str = Field(
        default="",
        description="Human-readable description.",
    )

    inputs: dict[str, int | str] = Field(
        default_factory=dict,
        description="Input signal values.",
    )

    expected_outputs: dict[str, int | str] = Field(
        default_factory=dict,
        description="Expected DUT outputs.",
    )

    delay: int = Field(
        default=10,
        ge=0,
        description="Simulation delay after applying inputs (ns).",
    )