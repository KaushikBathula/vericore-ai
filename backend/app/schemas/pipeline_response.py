"""
Schema for the Pipeline API response.
"""

from pydantic import BaseModel, Field


class PipelineResponse(BaseModel):
    """
    Response returned after executing the complete VeriCore AI pipeline.
    """

    success: bool = Field(
        ...,
        description="Whether the complete pipeline completed successfully.",
    )

    report_path: str = Field(
        ...,
        description="Path to the generated pipeline documentation report.",
    )

    message: str = Field(
        ...,
        description="Human-readable pipeline execution status.",
    )