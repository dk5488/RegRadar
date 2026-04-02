"""
RegRadar — Structured Logging Setup
Uses structlog for JSON-formatted, context-rich logging.
"""

import logging
import structlog
from app.core.config import get_settings

settings = get_settings()


def setup_logging():
    """Configure structlog + stdlib logging."""
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer()
            if settings.APP_ENV == "development"
            else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Also configure stdlib logging for third-party libraries
    logging.basicConfig(
        format="%(message)s",
        level=log_level,
    )


def get_logger(name: str = __name__):
    """Return a bound structlog logger."""
    return structlog.get_logger(name)
