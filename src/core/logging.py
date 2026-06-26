"""Application logging configuration.

Provides a single reusable `setup_logging()` function and a shared
`logger` instance, configured from `settings.log_level`.
"""

import logging
import sys

from .config import settings

LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"


def setup_logging(name: str = "legal_rag") -> logging.Logger:
    """Configure and return a console logger using the level from `settings.log_level`.

    Safe to call multiple times: any handlers already attached to the named
    logger are cleared first, so repeated calls never produce duplicate
    log lines.

    Args:
        name: Name of the logger to configure.

    Returns:
        The configured `logging.Logger` instance.
    """
    log = logging.getLogger(name)
    log.setLevel(settings.log_level)

    if log.handlers:
        log.handlers.clear()

    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(settings.log_level)
    handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT))

    log.addHandler(handler)
    log.propagate = False

    return log


logger: logging.Logger = setup_logging()
"""Shared application logger instance."""
