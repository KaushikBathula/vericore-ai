from fastapi import APIRouter

from backend.app.api import pipeline
from backend.app.api.routes import generation, health, projects


api_router = APIRouter()

api_router.include_router(
    health.router,
)

api_router.include_router(
    projects.router,
)

api_router.include_router(
    generation.router,
)

api_router.include_router(
    pipeline.router,
    prefix="/pipeline",
    tags=["Pipeline"],
)