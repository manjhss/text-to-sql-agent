import asyncio

from src.agent_core.agents.critic import executor_node
from src.agent_core.state import AgentState, default_state
from src.eval.cases.critic import validate_execute_cases


async def run_executor():
    for case in validate_execute_cases:
        result = await executor_node(
            AgentState(
                {
                    **default_state,
                    "raw_sql": case["input"]["raw_sql"],
                }
            )
        )

        print(f"\n{case['id']}")
        print("expected:", case["expected"])
        print("actual:", result)

        await asyncio.sleep(3)  # wait 3 seconds


asyncio.run(run_executor())
