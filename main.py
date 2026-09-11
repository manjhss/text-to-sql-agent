import uvicorn

from src.config.settings import settings


def main():
    uvicorn.run(
        "src.app:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )


if __name__ == "__main__":
    main()
