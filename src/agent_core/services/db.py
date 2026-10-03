from collections.abc import Iterable
from typing import Any

import sqlglot
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError

from config.settings import settings
from src.config.db import DB
from src.config.logger import logger


class DBService(DB):
    """manages db operations"""

    def __init__(self):
        self.db = SQLDatabase.from_uri(settings.database_url)
        self.inspector = inspect(create_engine(settings.database_url))

    def get_all_table_names(self) -> Iterable[str]:
        """get list of all table names in the db"""

        return self.db.get_usable_table_names()

    def get_tables_schema(self, tables: list[str]) -> str:
        """get tables schema by passing tables"""

        try:
            return self.db.get_table_info(tables)
        except Exception as e:
            logger.error(f"retrieving tables schema failed: {e}")
            return ""

    def get_table_metadata(self, table_name: str) -> dict[str, Any]:
        """get table metadata by passing table name"""

        try:
            columns = self.inspector.get_columns(table_name)
            pk = self.inspector.get_pk_constraint(table_name)
            fks = self.inspector.get_foreign_keys(table_name)
            indexes = self.inspector.get_indexes(table_name)

            return {
                "name": table_name,
                "columns": columns,
                "primary_key": pk,
                "foreign_keys": fks,
                "indexes": indexes,
            }
        except Exception as e:
            logger.error(f"getting metadata for failed: {table_name}: {e}")
            return {}

    def validate_sql_syntax(self, sql: str) -> tuple[bool, str | None]:
        """parse/validate sql syntax"""
        try:
            # using sqlglot to parse/validate
            parsed = sqlglot.parse_one(sql)
            if parsed:
                return True, None
            return False, "failed to parse SQL"
        except Exception as e:
            return False, str(e)

    async def execute_sql(self, sql: str) -> Any | None:
        """execute raw sql and return response"""

        try:
            # first validate syntax
            is_valid, syntax_error = self.validate_sql_syntax(sql)
            
            if not is_valid:
                return f"syntax error: {syntax_error}"

            # execute query
            async with self.engine.connect() as conn:
                result = await conn.execute(text(sql))

                # fetch results for SELECT queries
                if result.returns_rows:
                    rows = result.fetchall()
                    return rows
                else:
                    return (
                        f"query executed successfully. rows affected: {result.rowcount}"
                    )

        except SQLAlchemyError as e:
            logger.error(f"sql execution error: {e}")
            return None
        except Exception as e:
            logger.error(f"executing query failed: {e}")
            return None


db_service = DBService()
