import uvicorn

from src.config.logger import logger
from src.config.settings import settings


def main():
    logger.info(f"starting server on {settings.host}:{settings.port}")
    uvicorn.run(
        "src.app:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )


if __name__ == "__main__":
    main()
