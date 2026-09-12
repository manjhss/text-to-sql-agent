from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.cache.manager import cache_manager as cache
from src.config.logger import logger
from src.db.manager import db_manager as db
from src.features.health.route import router as health_router
from src.features.query.route import router as query_router


# app runs this once on startup and once on shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.startup()
    cache.startup()
    logger.info("application started")

    yield

    await db.dispose()
    cache.dispose()
    logger.info("application stopped")


app = FastAPI(
    title="text-to-sql agent",
    description="let user query db using natural language",
    lifespan=lifespan,
)


app.include_router(health_router)
app.include_router(query_router)
