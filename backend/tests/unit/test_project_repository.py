from sqlalchemy.orm import Session

from backend.app.repositories.project_repository import ProjectRepository
from backend.app.schemas.project import ProjectCreate


def test_project_repository_create_get_list_delete(db_session: Session) -> None:
    """ProjectRepository persists and deletes project metadata."""
    repository = ProjectRepository(db_session)

    project = repository.create(
        ProjectCreate(
            project_name="counter-demo",
            description="Repository test project.",
        )
    )

    assert project.id == 1
    assert repository.get(project.id) is not None
    assert len(repository.list()) == 1
    assert repository.delete(project.id) is True
    assert repository.get(project.id) is None
    assert repository.delete(project.id) is False
