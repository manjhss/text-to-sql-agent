from langchain_core.prompts import ChatPromptTemplate

from src.agent_core.prompts import SQL_GENERATION_PROMPT
from src.agent_core.services.llm import llm_service as llm
from src.agent_core.state import AgentState
from src.config.logger import logger


class SQLGeneratorAgent:
    """
    translates logical plans into valid SQL queries using Chain-of-Thought reasoning.
    """

    def __init__(self):
        self.llm_chat = llm.chat

        self.generation_prompt = ChatPromptTemplate.from_messages(
            [("system", SQL_GENERATION_PROMPT), ("user", "Generate the SQL query:")]
        )

    def _clean_sql(self, raw_sql: str) -> str:
        """
        return clean SQL output from LLM response"""

        # remove markdown code blocks
        sql = raw_sql.replace("```sql", "").replace("```", "").strip()

        # extract SQL from response (if it contains reasoning + SQL)
        # look for SQL keywords: SELECT, WITH, INSERT, UPDATE, DELETE
        lines = sql.split("\n")
        sql_start_idx = None

        for i, line in enumerate(lines):
            if any(
                keyword in line.upper()
                for keyword in ["SELECT", "WITH", "INSERT", "UPDATE", "DELETE"]
            ):
                sql_start_idx = i
                break

        if sql_start_idx is not None:
            sql = "\n".join(lines[sql_start_idx:])

        return sql.strip()

    def generate(self, state: AgentState) -> dict:
        """
        generate SQL query from plan and schema
        """

        logger.info("SQL GENERATOR: creating SQL query from plan")

        query = state["query"]
        plan = state.get("plan", "")
        schema_context = state.get("schema_context", "")

        if not schema_context:
            logger.error("no schema context available")
            return {
                "error": "cannot generate SQL without schema context",
                "should_retry": False,
            }

        try:
            # Step 1: generate SQL
            chain = self.generation_prompt | self.llm_chat
            response = chain.invoke(
                {"query": query, "plan": plan, "schema_context": schema_context}
            )

            # Step 2: clean the SQL output
            sql = self._clean_sql(response.content)

            logger.info(f"generated SQL ({len(sql)} characters)")
            logger.debug(f"SQL: {sql}")

            return {"raw_sql": sql}

        except Exception as e:
            logger.error(f"SQL generation error: {e}")
            return {"error": f"SQL generation failed: {str(e)}", "should_retry": False}


# node function for graph
def generator_node(state: AgentState) -> dict:
    """graph node wrapper for SQLGeneratorAgent"""

    agent = SQLGeneratorAgent()
    return agent.generate(state)
