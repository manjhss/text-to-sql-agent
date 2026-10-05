from typesafe_sdk._core.question_types import Choice

from src.agent_core.services.jev import jev_service as jev
from src.agent_core.state import AgentState, default_state
from src.config.logger import logger


def intent_classifier_node(state: AgentState) -> dict | None:
    query = state.get("query")

    try:
        response = jev.client.system_one(
            state=query,
            questions={
                "intent": Choice(
                    instructions="Determine whether the user's query is a database question that can be answered using the available tables.",
                    criteria={
                        "relevant": """
                                The user is asking to retrieve, calculate, compare, filter, or analyze
                                information stored in the database.

                                Available tables:
                                - customers
                                - behaviors
                                - products
                                - transactions

                                The query must express an information request about data in these tables.
                                Simply mentioning a database-related word, table name, or concept does not
                                make the query relevant.
                        """,
                        "irrelevant": """
                                The query is not asking for information from the database.

                                This includes:
                                - Statements that are not questions or data requests.
                                - General conversation or casual statements.
                                - Questions unrelated to the available data.
                                - Queries that merely mention words such as product, customer, transaction,
                                or behavior without asking to retrieve or analyze database information.
                        """,
                    },
                ),
            },
        )

        return {"query_type": response.answers["intent"].choice}
    except Exception as e:
        logger.error(f"intent classifier failed: {e}")
        return {"query_type": "irrelevant"}
