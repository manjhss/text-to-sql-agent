from time import sleep

from src.agent_core.agents.schema_retriever import schema_retriever
from src.agent_core.state import AgentState, default_state
from src.eval.test_cases.schema_retriver import schema_retriever_cases

for case in schema_retriever_cases:
    result = schema_retriever(
        AgentState(
            {
                **default_state,
                "query": case["input"]["query"],
                "plan": case["input"]["plan"],
            }
        )
    )

    print(f"\n{case['id']}")
    print("expected:", case["expected"]["relevant_tables"])
    print("actual:", result["relevant_tables"])

    sleep(3)  # wait 3 seconds
