from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.dependencies.database import get_database_session
from backend.app.main import app
from database.base import Base


@pytest.fixture()
def test_engine() -> Generator[Engine, None, None]:
    """Create an isolated in-memory SQLite engine for tests."""
    import backend.app.models.project  # noqa: F401

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture()
def db_session(test_engine: Engine) -> Generator[Session, None, None]:
    """Create a database session bound to the test engine."""
    testing_session_local = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
        expire_on_commit=False,
    )
    session = testing_session_local()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create a TestClient with database dependency overrides."""

    def override_get_database_session() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_database_session] = override_get_database_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
