from typing import Annotated

from fastapi import APIRouter, Depends, status

from backend.app.dependencies.services import get_generation_service
from backend.app.schemas.generation import (
    GenerationRequest,
    GenerationResponse,
)
from backend.app.services.generation_service import GenerationService

router = APIRouter(
    prefix="/generation",
    tags=["Generation"],
)


@router.post(
    "",
    response_model=GenerationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate RTL design from a natural language requirement",
)
def generate(
    request: GenerationRequest,
    service: Annotated[
        GenerationService,
        Depends(get_generation_service),
    ],
) -> GenerationResponse:

    requirement_spec, rtl_design = service.generate(
        request.requirement
    )

    return GenerationResponse(
        requirement_spec=requirement_spec,
        rtl_design=rtl_design,
    )