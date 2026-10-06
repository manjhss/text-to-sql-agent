from time import sleep

from src.agent_core.input_guardrail import input_guardrail_node
from src.agent_core.state import AgentState, default_state
from src.eval.cases.input_guardrail import input_guardrail_cases

for case in input_guardrail_cases:
    result = input_guardrail_node(
        AgentState({**default_state, "query": case["input"]["query"]})
    )

    print(f"\n{case['id']}")
    print("expected:", case["expected"])
    print("actual:", result)

    sleep(3)  # wait 3 seconds
