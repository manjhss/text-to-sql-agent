from typing import Literal

from src.agent_core.state import AgentState
from src.config.logger import logger


def route_execution(state: AgentState) -> Literal["debug", "end"]:
    """
    determines the next step in the workflow after query execution.

    decision flow:
    - if max iterations reached: end with error
    - if error occured: attempt to debug
    """

    # if max iterations reached, stop
    if state.get("iterations", 0) >= settings.max_iterations:
        logger.warning(
            f"✗ max iterations ({settings.max_iterations}) reached - ending workflow"
        )
        return "end"

    # if should_retry flag is False, stop
    if not state.get("should_retry", True):
        logger.warning("✗ retry flag is False - ending workflow")
        return "end"

    # otherwise, attempt correction
    logger.info(f"↻ attempting correction (iteration {state.get('iterations', 0) + 1})")
    return "debug"