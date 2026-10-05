from time import sleep

from src.agent_core.intent_classifier import intent_classifier_node
from src.agent_core.state import AgentState, default_state
from src.eval.cases.intent_classifier import intent_classifier_cases

for case in intent_classifier_cases:
    result = intent_classifier_node(
        AgentState({**default_state, "query": case["input"]["query"]})
    )

    print(f"\n{case['id']}")
    print("expected:", case["expected"])
    print("actual:", result)

    sleep(3)  # wait 3 seconds
