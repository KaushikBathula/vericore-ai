"""Schema representing the result of an RTL simulation."""

from pydantic import BaseModel, Field


class SimulationResult(BaseModel):
    """Represents the outcome of compiling and simulating RTL."""

    compile_success: bool = Field(
        ...,
        description="Whether compilation completed successfully.",
    )

    simulation_success: bool = Field(
        ...,
        description="Whether simulation completed successfully.",
    )

    stdout: str = Field(
        default="",
        description="Combined standard output.",
    )

    stderr: str = Field(
        default="",
        description="Combined standard error.",
    )

    execution_time: float = Field(
        default=0.0,
        ge=0.0,
        description="Simulation execution time in seconds.",
    )

    waveform_path: str | None = Field(
        default=None,
        description="Generated waveform (.vcd) file path.",
    )

    compiler_output: str = Field(
        default="",
        description="Compiler output from Icarus Verilog.",
    )

    simulation_output: str = Field(
        default="",
        description="Simulation runtime output.",
    )