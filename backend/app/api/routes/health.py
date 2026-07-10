from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.app.dependencies.database import get_database_session
from backend.app.schemas.common import HealthResponse

router = APIRouter(tags=["Health"])

APP_VERSION = "0.1.0"


@router.get("/health", response_model=HealthResponse, summary="Health check")
def health_check(
    db: Annotated[Session, Depends(get_database_session)],
) -> HealthResponse:
    """Return service health and database connectivity status."""
    database_connectivity = True
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        database_connectivity = False

    return HealthResponse(
        status="ok" if database_connectivity else "degraded",
        version=APP_VERSION,
        database_connectivity=database_connectivity,
    )
