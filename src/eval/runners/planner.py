from time import sleep

from src.agent_core.agents.planner import planner_node
from src.agent_core.state import AgentState, default_state
from src.eval.cases.planner import planner_cases

for case in planner_cases:
    result = planner_node(
        AgentState(
            {
                **default_state,
                "query": case["input"]["query"],
            }
        )
    )

    print(f"\n{case['id']}")
    print("expected:", case["expected"])
    print("actual:", result["plan_steps"])

    sleep(3)  # wait 3 seconds
