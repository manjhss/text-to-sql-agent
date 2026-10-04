from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

from src.agent_core.prompts import DEBUG_SQL_FAILURE_PROMPT
from src.agent_core.services.db import db_service as db
from src.agent_core.services.llm import llm_service as llm
from src.agent_core.state import AgentState
from src.config.settings import settings


class CriticAgent:
    """
    validates, executes, and corrects SQL queries
    """

    def __init__(self):
        self.llm_chat = llm.chat

        # prompt for debugging failure
        self.debug_failure_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", DEBUG_SQL_FAILURE_PROMPT),
                ("user", "Fix the query:"),
            ]
        )

    def _classify_error(self, error_msg: str) -> str:
        """
        classify error type for better handling
        """

        error_lower = error_msg.lower()

        if "column" in error_lower and (
            "does not exist" in error_lower or "not found" in error_lower
        ):
            return "column_not_found"
        elif "table" in error_lower and (
            "does not exist" in error_lower or "not found" in error_lower
        ):
            return "table_not_found"
        elif "syntax" in error_lower:
            return "syntax_error"
        elif "ambiguous" in error_lower:
            return "ambiguous_column"
        elif "timeout" in error_lower:
            return "timeout"
        else:
            return "runtime_error"

    def _format_result_preview(self, result, max_rows: int = 5) -> str:
        """
        format query result for display
        """
        
        if isinstance(result, str):
            return result

        if not result:
            return "query returned no results"

        try:
            # if result is a list of Row objects
            if hasattr(result[0], "_mapping"):
                rows = [dict(row._mapping) for row in result[:max_rows]]
                preview = f"Returned {len(result)} row(s). Preview:\n"
                for i, row in enumerate(rows, 1):
                    preview += f"Row {i}: {row}\n"

                if len(result) > max_rows:
                    preview += f"... ({len(result) - max_rows} more rows)"

                return preview
            else:
                return str(result[:max_rows])

        except Exception as e:
            logger.warning(f"could not format result: {e}")
            return str(result)[:500]  # truncate to 500 chars

    async def execute_and_validate(self, state: AgentState) -> dict:
        """
        execute SQL query and handle results/errors
        """

        logger.info("CRITIC: executing and validating SQL query")

        raw_sql = state.get("raw_sql")
        if not raw_sql:
            return {"error": "no SQL query to execute", "should_retry": False}

        try:
            # execute the query
            result, error = await db.execute_sql(raw_sql)

            if error:
                # Query failed - prepare for debugger
                logger.warning(f"query execution failed: {error}")
                error_type = self._classify_error(error)

                return {
                    "error": error,
                    "error_type": error_type,
                    "query_result": None,
                    "should_retry": True,
                }
            else:
                # query succeeded
                logger.info("query executed successfully")
                result_preview = self._format_result_preview(result)

                return {
                    "query_result": result_preview,
                    "error": None,
                    "should_retry": False,
                }

        except Exception as e:
            logger.error(f"execution error: {e}")
            return {"error": str(e), "error_type": "runtime", "should_retry": True}

    def debug_and_fix(self, state: AgentState) -> dict:
        """
        analyze error and generate corrected SQL
        """

        logger.info("CRITIC: bebugging on error and fixing SQL")

        iterations = state.get("iterations", 0)

        # Check if we've exceeded max iterations
        if iterations >= settings.max_iterations:
            logger.error(f"max iterations ({settings.max_iterations}) reached")
            return {
                "should_retry": False,
                "error": f"failed to generate valid SQL after {settings.max_iterations} attempts",
            }

        query = state["query"]
        plan = state.get("plan", "")
        schema_context = state.get("schema_context", "")
        raw_sql = state.get("raw_sql", "")
        error = state.get("error", "")

        try:
            chain = self.debug_failure_prompt | self.llm_chat

            response = chain.invoke(
                {
                    "query": query,
                    "plan": plan,
                    "schema_context": schema_context,
                    "raw_sql": raw_sql,
                    "error": error,
                }
            )

            # clean the fixed SQL
            from agents.generator import SQLGeneratorAgent

            generator = SQLGeneratorAgent()
            fixed_sql = generator._clean_sql(response.content)

            logger.info(f"generated corrected SQL (iteration {iterations + 1})")
            logger.debug(f"fixed SQL: {fixed_sql}")

            return {
                "raw_sql": fixed_sql,
                "iterations": iterations + 1,
                "should_retry": True,
            }

        except Exception as e:
            logger.error(f"reflection error: {e}")
            return {
                "error": f"failed to correct SQL: {str(e)}",
                "iterations": iterations + 1,
                "should_retry": False,
            }


# node functions for graph
async def executor_node(state: AgentState) -> dict:
    """graph node wrapper for execution"""

    agent = CriticAgent()
    return await agent.execute_and_validate(state)


def debugger_node(state: AgentState) -> dict:
    """graph node wrapper for correction"""

    agent = CriticAgent()
    return agent.debug_and_fix(state)
