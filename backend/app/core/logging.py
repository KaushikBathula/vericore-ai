import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from backend.app.core.config import Settings, get_settings

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(settings: Settings | None = None) -> None:
    """Configure console and rotating file logging for the application."""
    app_settings = settings or get_settings()
    logs_dir = app_settings.logs_dir
    logs_dir.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(app_settings.log_level)
    root_logger.handlers.clear()

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(app_settings.log_level)

    file_handler = RotatingFileHandler(
        filename=Path(logs_dir) / "vericore.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(app_settings.log_level)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger instance."""
    return logging.getLogger(name)
