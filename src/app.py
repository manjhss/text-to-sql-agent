from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config.logger import logger
from src.db.manager import db_manager as db
from src.features.health.route import router as health_router


# FastAPI runs this once on startup and once on shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    db.check_connection()
    logger.info("application started")

    yield

    db.dispose()
    logger.info("application stopped")


app = FastAPI(
    title="text-to-sql agent",
    description="let user query db using natural language",
    lifespan=lifespan,
)


app.include_router(health_router)
