"""
Schema for Pipeline API requests.
"""

from pydantic import BaseModel, Field


class PipelineRequest(BaseModel):
    """
    Request for executing the complete VeriCore AI pipeline.
    """

    requirement: str = Field(
        ...,
        min_length=1,
        description="Natural-language hardware specification.",
    )