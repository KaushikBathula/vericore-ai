from typing import Any

from pydantic import BaseModel, ConfigDict


class BaseResponse(BaseModel):
    """Standard response envelope for simple API operations."""

    success: bool
    message: str


class ErrorResponse(BaseModel):
    """Standard API error response body."""

    error: str
    detail: str | list[dict[str, Any]] | None = None


class HealthResponse(BaseModel):
    """Health-check response body."""

    status: str
    version: str
    database_connectivity: bool

    model_config = ConfigDict(from_attributes=True)
