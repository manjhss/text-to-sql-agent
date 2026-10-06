import sqlite3

import aiosqlite
from sqlalchemy import text

from src.config.logger import logger
from src.config.settings import settings


class DB:
    """manages db connections"""

    def __init__(self):
        self.database_url = settings.database_url
        self.conn: aiosqlite.Connection | None = None

    def _authorizer(self, action, arg1, arg2, db_name, trigger_name):
        """
        add db-level security layer. prevents mutation operations - drop table, insert
        """

        denied = {
            sqlite3.SQLITE_INSERT,
            sqlite3.SQLITE_UPDATE,
            sqlite3.SQLITE_DELETE,
            sqlite3.SQLITE_CREATE_TABLE,
            sqlite3.SQLITE_CREATE_INDEX,
            sqlite3.SQLITE_CREATE_TRIGGER,
            sqlite3.SQLITE_CREATE_VIEW,
            sqlite3.SQLITE_DROP_TABLE,
            sqlite3.SQLITE_DROP_INDEX,
            sqlite3.SQLITE_DROP_TRIGGER,
            sqlite3.SQLITE_DROP_VIEW,
            sqlite3.SQLITE_ALTER_TABLE,
            sqlite3.SQLITE_ATTACH,
            sqlite3.SQLITE_DETACH,
        }

        if action in denied:
            return sqlite3.SQLITE_DENY

        return sqlite3.SQLITE_OK

    async def configure_security(self, conn: aiosqlite.Connection):
        """
        configure authorizer
        """

        await conn.set_authorizer(authorizer_callback=self._authorizer)

    async def startup(self):
        """create tables and run a cheap query to check db connection"""

        try:
            conn = aiosqlite.connect(self.database_url)
            await self.configure_security(conn=conn)

            await conn.execute(text("SELECT 1"))
            logger.info("database connection ok")
        except Exception:
            logger.exception("db startup failed")
            raise

    async def dispose(self):
        """dispose db connection"""

        if self.conn:
            await self.conn.close()
            logger.info("database connection disposed")


db = DB()
