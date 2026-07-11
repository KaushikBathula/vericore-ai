from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.dependencies.database import get_database_session
from backend.app.repositories.project_repository import ProjectRepository
from backend.app.services.project_service import ProjectService
from backend.app.services.generation_service import GenerationService

def get_project_service(
    db: Annotated[Session, Depends(get_database_session)],
) -> ProjectService:
    """Build a project service for the current request."""
    repository = ProjectRepository(db)
    return ProjectService(repository)
def get_generation_service() -> GenerationService:
    """
    Build a generation service.
    """
    return GenerationService()