from collections.abc import Iterator

from loguru import logger
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from src.config.settings import settings


class DBManager:
    """manages db connections and operations"""

    def __init__(self):
        self.engine = create_engine(
            settings.database_url,
            echo=False
        )

    def check_connection(self):
        """run a cheap query to check db connection"""

        try:
            with self.engine.begin() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("database connection ok")
        except Exception:
            logger.exception("database connection failed")
            raise

    def get_session(self) -> Iterator[Session]:
        """yield a db session and close it when the caller is done"""

        with Session(self.engine) as session:
            try:
                yield session
            finally:
                session.close()

    def dispose(self):
        """dispose db connection"""

        self.engine.dispose()
        logger.info("database connections disposed")


db_manager = DBManager()
