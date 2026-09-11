import sys

from loguru import logger

logger.remove()
logger.add(
    sys.stderr,
    level="INFO",
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level}</level> | "
        "<level>{message}</level>"
    ),
)

__all__ = ["logger"]
