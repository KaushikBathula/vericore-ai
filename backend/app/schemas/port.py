from typing import Literal

from pydantic import BaseModel, Field


class Port(BaseModel):
    """
    Represents a hardware port.
    """

    signal_name: str = Field(
        ...,
        description="Name of the signal."
    )

    signal_width: int = Field(
        default=1,
        ge=1,
        description="Width of the signal in bits."
    )

    signal_type: str = Field(
        default="logic",
        description="Signal data type."
    )

    direction: Literal["input", "output"] = Field(
        ...,
        description="Port direction."
    )