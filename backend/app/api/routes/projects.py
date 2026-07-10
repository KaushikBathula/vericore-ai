from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from backend.app.dependencies.services import get_project_service
from backend.app.schemas.common import BaseResponse
from backend.app.schemas.project import ProjectCreate, ProjectResponse
from backend.app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create project metadata",
)
def create_project(
    project_data: ProjectCreate,
    service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectResponse:
    """Create project metadata without invoking RTL generation."""
    return ProjectResponse.model_validate(service.create_project(project_data))


@router.get(
    "",
    response_model=list[ProjectResponse],
    summary="List project metadata",
)
def list_projects(
    service: Annotated[ProjectService, Depends(get_project_service)],
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
) -> list[ProjectResponse]:
    """List project metadata records."""
    projects = service.list_projects(offset=offset, limit=limit)
    return [ProjectResponse.model_validate(project) for project in projects]


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get project metadata",
)
def get_project(
    project_id: int,
    service: Annotated[ProjectService, Depends(get_project_service)],
) -> ProjectResponse:
    """Return one project metadata record."""
    return ProjectResponse.model_validate(service.get_project(project_id))


@router.delete(
    "/{project_id}",
    response_model=BaseResponse,
    summary="Delete project metadata",
)
def delete_project(
    project_id: int,
    service: Annotated[ProjectService, Depends(get_project_service)],
) -> BaseResponse:
    """Delete project metadata without touching generated artifacts."""
    service.delete_project(project_id)
    return BaseResponse(success=True, message="Project deleted successfully.")
