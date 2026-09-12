from collections.abc import AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.config.logger import logger
from src.config.settings import settings
from src.db.modals import Base


class DBManager:
    """manages db connections and operations"""

    def __init__(self):
        self.engine = create_async_engine(settings.database_url, echo=False)

    async def startup(self):
        """create tables and run a cheap query to check db connection"""

        async with self.engine.begin() as conn:
            try:
                await conn.run_sync(Base.metadata.create_all)
                logger.info("db tables ready")

                await conn.execute(text("SELECT 1"))
                logger.info("database connection ok")
            except Exception:
                logger.exception("db startup failed")
                raise

    async def get_session(self) -> AsyncIterator[AsyncSession]:
        """return async db session"""

        async with AsyncSession(self.engine) as session:
            yield session

    async def dispose(self):
        """dispose db connection"""

        await self.engine.dispose()
        logger.info("database connection disposed")


db_manager = DBManager()
