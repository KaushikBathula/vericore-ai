from pydantic import BaseModel, Field


class Operation(BaseModel):
    """
    Represents one supported hardware operation.
    """

    operation_name: str = Field(
        ...,
        description="Name of the operation."
    )

    description: str | None = Field(
        default=None,
        description="Engineering description of the operation."
    )

    function: str | None = Field(
        default=None,
        description="Optional implementation hint from the LLM."
    )