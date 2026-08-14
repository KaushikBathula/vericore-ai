"""
Pipeline API.

Exposes the complete VeriCore AI pipeline.
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException

from backend.app.schemas.pipeline_request import PipelineRequest
from backend.app.schemas.pipeline_response import PipelineResponse
from backend.app.services.pipeline_service import PipelineService

router = APIRouter()


@router.post(
    "/run",
    response_model=PipelineResponse,
)
def run_pipeline(
    request: PipelineRequest,
) -> PipelineResponse:
    """
    Execute the complete VeriCore AI pipeline.
    """

    print("\n############################################")
    print("########## PIPELINE API HIT ################")
    print("############################################\n")

    try:
        service = PipelineService()

        print("PipelineService Object :", service)
        print("PipelineService Class  :", PipelineService)
        print("PipelineService Module :", PipelineService.__module__)
        print("Requirement Received   :", request.requirement)
        print()

        report = service.execute(
            requirement_text=request.requirement,
            output_directory=Path("generated_projects"),
        )

        print("\n########## PIPELINE COMPLETED ##########\n")

        return PipelineResponse(
            success=report.success,
            report_path=str(Path("generated_projects")),
            message="Pipeline executed successfully.",
        )


    except Exception as exc:

        print("\n########## PIPELINE FAILED ##########")
        print(exc)
        print("#####################################\n")

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )