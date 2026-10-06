from typing import Literal

from src.agent_core.state import AgentState
from src.config.logger import logger


def route_intent(state: AgentState) -> Literal["relevant", "irrelevant"]:
    """
    determines whether to continue based on query relevance
    """

    if state.get("query_type", "irrelevant") == "irrelevant":
        logger.warning("query is irrelevant - ending workflow")
        return "irrelevant"

    logger.info("query is relevant - proceeding to input guardrail")
    return "relevant"
