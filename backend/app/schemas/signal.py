from enum import Enum

from pydantic import BaseModel, Field


class SignalType(str, Enum):
    """
    Supported RTL signal categories.
    """

    INPUT = "input"
    OUTPUT = "output"
    WIRE = "wire"
    REG = "reg"
    LOGIC = "logic"
    INTERNAL = "internal"


class Signal(BaseModel):
    """
    Represents a generic RTL signal.

    This model is reused throughout the RTL generation
    pipeline for ports, internal wires, registers,
    and intermediate signals.
    """

    signal_name: str = Field(
        ...,
        description="Signal name."
    )

    signal_width: int = Field(
        default=1,
        ge=1,
        description="Signal width in bits."
    )

    signed: bool = Field(
        default=False,
        description="Whether the signal is signed."
    )

    signal_type: SignalType = Field(
        ...,
        description="RTL signal type."
    )

    default_value: str | None = Field(
        default=None,
        description="Optional default initialization."
    )

    description: str = Field(
        default="",
        description="Human-readable signal description."
    )