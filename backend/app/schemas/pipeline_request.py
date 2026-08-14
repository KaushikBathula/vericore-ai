from pydantic import BaseModel, Field


class PipelineRequest(BaseModel):
    """
    Request for executing the complete VeriCore AI pipeline.
    """

    requirement: str = Field(
        ...,
        description="Natural language hardware specification.",
    )