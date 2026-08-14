"""
VeriCore AI FastAPI application entry point.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.router import api_router
from backend.app.core.config import get_settings
from backend.app.core.exceptions import register_exception_handlers
from backend.app.core.logging import configure_logging, get_logger
from database.session import init_db


APP_TITLE = "VeriCore AI"
APP_DESCRIPTION = (
    "Autonomous RTL Design and Verification Engineer backend API."
)
APP_VERSION = "0.1.0"


settings = get_settings()

configure_logging(settings)

logger = get_logger(__name__)


def ensure_runtime_directories() -> None:
    """Create runtime directories required by the backend."""

    settings.generated_projects_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    settings.logs_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    settings.outputs_dir.mkdir(
        parents=True,
        exist_ok=True,
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Handle application startup and shutdown tasks."""

    logger.info(
        "Starting %s %s",
        APP_TITLE,
        APP_VERSION,
    )

    ensure_runtime_directories()

    init_db()

    logger.info(
        "Runtime directories and database initialized"
    )

    yield

    logger.info(
        "Shutting down %s",
        APP_TITLE,
    )


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title=APP_TITLE,
        description=APP_DESCRIPTION,
        version=APP_VERSION,
        debug=settings.debug,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    app.include_router(
        api_router,
        prefix=settings.api_prefix,
    )

    return app


app = create_app()