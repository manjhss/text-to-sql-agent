from time import sleep

from src.agent_core.agents.generator import generator_node
from src.agent_core.state import AgentState, default_state
from src.eval.test_cases.generator import generator_cases

for case in generator_cases:
    result = generator_node(
        AgentState(
            {
                **default_state,
                "query": case["input"]["query"],
                "plan": case["input"]["plan"],
                "schema_context": case["input"]["schema_context"],
            }
        )
    )

    print(f"\n{case['id']}")
    print("expected:", case["expected"])
    print("actual:", result)

    sleep(3)  # wait 3 seconds
