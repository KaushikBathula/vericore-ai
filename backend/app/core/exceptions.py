from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.app.core.logging import get_logger

logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """Register global API exception handlers."""

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        logger.warning("Validation error on %s: %s", request.url.path, exc.errors())
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": "VALIDATION_ERROR", "detail": exc.errors()},
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException,
    ) -> JSONResponse:
        detail = exc.detail if isinstance(exc.detail, str) else "HTTP error"
        logger.info("HTTP error on %s: %s", request.url.path, detail)
        error_code = "NOT_FOUND" if exc.status_code == 404 else "HTTP_ERROR"
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": error_code, "detail": exc.detail},
        )

    @app.exception_handler(HTTPException)
    async def fastapi_http_exception_handler(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        logger.info("HTTP error on %s: %s", request.url.path, exc.detail)
        error_code = "NOT_FOUND" if exc.status_code == 404 else "HTTP_ERROR"
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": error_code, "detail": exc.detail},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger.exception("Unhandled error on %s: %s", request.url.path, exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "INTERNAL_SERVER_ERROR",
                "detail": "Internal server error",
            },
        )
