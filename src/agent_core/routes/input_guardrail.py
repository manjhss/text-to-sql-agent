from typing import Literal

from src.agent_core.state import AgentState
from src.config.logger import logger


def route_guardrail(state: AgentState) -> Literal["safe", "unsafe"]:
    """
    determines whether to continue based on input safety
    """

    if state.get("input_guardrail", "unsafe") == "unsafe":
        logger.warning("input is unsafe - ending workflow")
        return "unsafe"

    logger.info("input is safe - proceeding to planner")
    return "safe"
