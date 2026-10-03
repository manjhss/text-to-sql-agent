from langchain_core.prompts import ChatPromptTemplate

from src.agent_core.prompts import COLUMN_SELECTION_PROMPT, TABLE_SELECTION_PROMPT
from src.agent_core.services.db import db_service as db
from src.agent_core.services.llm import llm_service as llm
from src.agent_core.state import AgentState
from src.config.logger import logger


class SchemaRetrieverAgent:
    """
    identifies only the relevant tables and columns needed for the query.
    """

    def __init__(self):
        self.llm_chat = llm.chat

        # system prompt for table selection
        self.table_selection_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", TABLE_SELECTION_PROMPT),
                (
                    "user",
                    """
                        Query: {query}
                        Plan: {plan}
                        Available Tables: {all_tables}
                        Return comma-separated table names:
                    """,
                ),
            ]
        )

        # prompt for column selection (optional, currently not used)
        self.column_selection_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", COLUMN_SELECTION_PROMPT),
                (
                    "user",
                    """
                        Plan: {plan}
                        Schema: {schema}
                        Return JSON with required columns:
                    """,
                ),
            ]
        )

    def select_tables(self, query: str, plan: str, all_tables: list[str]) -> list[str]:
        """
        return relevant tables using LLM reasoning"""

        try:
            chain = self.table_selection_prompt | self.llm_chat
            response = chain.invoke(
                {
                    "query": query,
                    "plan": plan,
                    "all_tables": ", ".join(all_tables),
                }
            )

            # parse comma-separated table names
            selected = [t.strip() for t in response.content.split(",")]
            # Filter out any invalid table names
            selected = [t for t in selected if t in all_tables]

            logger.info(
                f"selected {len(selected)} tables from {len(all_tables)} available"
            )
            return selected

        except Exception as e:
            logger.error(f"table selection error: {e}")
            # fallback: return first 10 tables
            return all_tables[:10]

    def retrieve_schema(self, state: AgentState) -> dict:
        """
        retrieve and prune schema information to only relevant tables
        """

        logger.info("SCHEMA RETRIEVER: retrieving relevant tables and schema")

        query = state["query"]
        plan = state.get("plan", "")

        try:
            # Step 1: get all available tables
            all_tables = db.get_all_table_names()
            logger.info(f"database has {len(all_tables)} tables")

            # Step 2: select relevant tables using LLM
            if plan:
                selected_tables = self.select_tables(query, plan, all_tables)
            else:
                # Fallback: use first 10 tables if no plan available
                selected_tables = all_tables[:10]

            # Step 3: retrieve data schema for selected tables
            schema_context = db.get_tables_schema(selected_tables)

            # Step 4: get metadata (keys, indexes, etc.)
            schema_metadata = {}
            for table in selected_tables:
                metadata = db.get_table_metadata(table)
                schema_metadata[table] = metadata

            logger.info(
                f"selected {len(selected_tables)} tables: {', '.join(selected_tables)}"
            )

            return {
                "relevant_tables": selected_tables,
                "schema_context": schema_context,
                "schema_metadata": schema_metadata,
            }

        except Exception as e:
            logger.error(f"schema retrieval error: {e}")
            return {
                "error": f"schema retrieval failed: {str(e)}",
                "should_retry": False,
            }


# node function for graph
def schema_linker_node(state: AgentState) -> dict:
    """graph node wrapper for SchemaRetrieverAgent"""

    agent = SchemaRetrieverAgent()
    return agent.retrieve_schema(state)
