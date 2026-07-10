from collections.abc import Generator

from sqlalchemy.orm import Session

from database.session import get_db


def get_database_session() -> Generator[Session, None, None]:
    """Provide a SQLAlchemy session to FastAPI dependencies."""
    yield from get_db()
