from typing import Literal

from langgraph.graph import END, StateGraph

from src.agent_core.agents.critic import debugger_node, executor_node
from src.agent_core.agents.generator import generator_node
from src.agent_core.agents.planner import planner_node
from src.agent_core.agents.schema_retriever import schema_retriever
from src.agent_core.intent_classifier import intent_classifier_node
from src.agent_core.state import AgentState, default_state
from src.config.logger import logger
from src.config.settings import settings


def should_continue(
    state: AgentState,
) -> Literal["relevant", "irrelevant", "debug", "end"]:
    """
    determines the next step in the workflow after query execution.

    decision flow:
    - if max iterations reached: end with error
    - if error occured: attempt to debug
    """
    # if query is relevant
    if state.get("query_type", "irrelevant") == "relevant":
        logger.warning("query is relevant. proceed")
        return "relevant"

    # if query is irrelevant
    if state.get("query_type", "irrelevant") == "irrelevant":
        logger.warning("query is irrelevant. don't proceed")
        return "irrelevant"

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


def build_graph() -> StateGraph:
    """
    builds the langgraph workflow for the Text-to-SQL agent

    workflow:
        1. Plan: Break down the question into logical steps
        2. Schema Retriever: Find relevant tables/columns
        3. Generate: Write SQL query
        4. Execute: Run query and validate
        5. On error: Debug and retry (up to max_iterations)
        6. On success: End
    """

    logger.info("building Text-to-SQL agent graph...")

    # initialize the state graph
    workflow = StateGraph(AgentState)

    # === ADD NODES ===
    workflow.add_node(
        "intent_classifier", intent_classifier_node
    )  # classify query intent
    workflow.add_node("planner", planner_node)  # decompose question into steps
    workflow.add_node("schema_retriever", schema_retriever)  # find relevant tables
    workflow.add_node("generator", generator_node)  # generate SQL
    workflow.add_node("executor", executor_node)  # execute and validate
    workflow.add_node("debugger", debugger_node)  # fix errors if any
    # later add two more nodes - intent_classifier and input/output guards

    # === DEFINE WORKFLOW ===
    workflow.set_entry_point("intent_classifier")

    # after execution, decide: error (debug), or give up (end)
    workflow.add_conditional_edges(
        "intent_classifier",
        should_continue,
        {"irrelevant": END, "relevant": "planner"},
    )

    # linear flow through the pipeline
    workflow.add_edge("planner", "schema_retriever")
    workflow.add_edge("schema_retriever", "generator")
    workflow.add_edge("generator", "executor")

    # after execution, decide: error (debug), or give up (end)
    workflow.add_conditional_edges(
        "executor",
        should_continue,
        {"end": END, "debug": "debugger"},
    )

    # after debugging, retry execution
    workflow.add_edge("debugger", "executor")

    logger.info("graph built successfully")
    return workflow


def compile_graph():
    """
    compile the workflow graph
    """

    workflow = build_graph()
    app = workflow.compile()
    logger.info("graph compiled and ready")

    return app


# create global graph instance
graph = compile_graph()


async def run_agent(query: str) -> dict:
    """
    execute the Text-to-SQL agent for a given query.
    """

    logger.info("running Text-to-SQL Agent")
    logger.info(f"Query: {query}")

    # initialize state
    initial_state: AgentState = {**default_state, "query": query}

    try:
        final_state = await graph.ainvoke(initial_state)

        # log summary
        if final_state.get("error"):
            logger.error(f"✗ agent failed: {final_state['error']}")
        else:
            logger.info("✓ agent succeeded")
            logger.info(f"SQL: {final_state.get('raw_sql', 'N/A')}")

        return final_state

    except Exception as e:
        logger.error(f"graph execution error: {e}")
        return {**initial_state, "error": str(e), "should_retry": False}
