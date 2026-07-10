from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.project import Project
from backend.app.schemas.project import ProjectCreate


class ProjectRepository:
    """Repository for project metadata persistence."""

    def __init__(self, db: Session) -> None:
        """Initialize repository with a database session."""
        self._db = db

    def create(self, project_data: ProjectCreate) -> Project:
        """Create and persist a project record."""
        project = Project(
            project_name=project_data.project_name,
            description=project_data.description,
            status="created",
        )
        self._db.add(project)
        self._db.commit()
        self._db.refresh(project)
        return project

    def get(self, project_id: int) -> Project | None:
        """Return a project by ID when it exists."""
        return self._db.get(Project, project_id)

    def list(self, offset: int = 0, limit: int = 100) -> list[Project]:
        """Return projects ordered by newest first."""
        statement = (
            select(Project)
            .order_by(Project.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(self._db.scalars(statement).all())

    def delete(self, project_id: int) -> bool:
        """Delete a project by ID and return whether it existed."""
        project = self.get(project_id)
        if project is None:
            return False
        self._db.delete(project)
        self._db.commit()
        return True
