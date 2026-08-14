from pydantic import BaseModel


class PipelineResponse(BaseModel):
    """
    Response returned after pipeline execution.
    """

    success: bool

    report_path: str

    message: str