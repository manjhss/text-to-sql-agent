from langchain_core.prompts import ChatPromptTemplate

from src.agent_core.prompts import PLANNER_PROMPT
from src.agent_core.services.llm import llm_service as llm
from src.agent_core.state import AgentState
from src.config.logger import logger


class PlannerAgent:
    """decomposes natural language questions into structured logical plans"""
    
    def __init__(self):
        self.llm_chat = llm.chat
        
        # system prompt for logical planning
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", PLANNER_PROMPT),
            ("user", "{query}")
        ])
        
        self.chain = self.prompt | self.llm_chat
    
    def plan(self, state: AgentState) -> dict:
        """generate a logical plan for the question."""

        logger.info("PLANNER: decomposing question into logical steps")
        query = state["query"]
        
        try:
            response = self.chain.invoke({"query": query})
            plan = response.content
            
            # extract numbered steps from the plan
            import re
            steps = re.findall(r'^\d+\..*$', plan, re.MULTILINE)
            logger.info(f"generated plan with {len(steps)} steps")
            
            return {
                "plan": plan,
                "plan_steps": steps,
                "iterations": 0,
                "should_retry": True
            }
        except Exception as e:
            logger.error(f"planner error: {e}")
            return {"error": f"planning failed: {str(e)}", "should_retry": False}


# node function for graph
def planner_node(state: AgentState) -> dict:
    """graph node wrapper for PlannerAgent"""

    agent = PlannerAgent()
    return agent.plan(state)