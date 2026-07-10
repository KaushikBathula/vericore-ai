from fastapi import HTTPException, status

from backend.app.models.project import Project
from backend.app.repositories.project_repository import ProjectRepository
from backend.app.schemas.project import ProjectCreate


class ProjectService:
    """Business operations for project metadata."""

    def __init__(self, repository: ProjectRepository) -> None:
        """Initialize service with a project repository."""
        self._repository = repository

    def create_project(self, project_data: ProjectCreate) -> Project:
        """Create a project metadata record."""
        return self._repository.create(project_data)

    def get_project(self, project_id: int) -> Project:
        """Return a project or raise a domain-level HTTP error."""
        project = self._repository.get(project_id)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} was not found.",
            )
        return project

    def list_projects(self, offset: int = 0, limit: int = 100) -> list[Project]:
        """List projects with pagination bounds."""
        bounded_limit = min(max(limit, 1), 100)
        bounded_offset = max(offset, 0)
        return self._repository.list(offset=bounded_offset, limit=bounded_limit)

    def delete_project(self, project_id: int) -> None:
        """Delete a project or raise when it does not exist."""
        deleted = self._repository.delete(project_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project {project_id} was not found.",
            )
