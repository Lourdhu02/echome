import logging
from typing import TypedDict, List, Dict, Any, Union

from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    """The state of the ECHOME orchestrator graph."""
    messages: List[BaseMessage]
    intent: str
    next_agent: str
    results: Dict[str, Any]

class Orchestrator:
    """
    ECHOME Intent Classifier and Agent Router (L3 Orchestration).
    Uses LangGraph to route inputs to specialist agents.
    """

    def __init__(self):
        self.workflow = StateGraph(AgentState)
        self._build_graph()

    def _classify_intent(self, state: AgentState) -> Dict[str, Any]:
        """Classifies the user intent into system_task, conversation, or hybrid."""
        last_message = state['messages'][-1].content.lower()
        
        # Simple rule-based classification for demonstration
        # In production, this is a lightweight LLM call (e.g., Mistral-7B)
        intent = "conversation"
        next_agent = "tech"
        
        if any(cmd in last_message for cmd in ["run", "ls", "pwd", "grep", "mkdir"]):
            intent = "system_task"
            next_agent = "bash"
        
        logger.info(f"Classified intent: {intent}, Next agent: {next_agent}")
        return {"intent": intent, "next_agent": next_agent}

    def _execute_agent(self, state: AgentState) -> Dict[str, Any]:
        """Dispatches the task to the selected specialist agent."""
        agent_name = state['next_agent']
        # For demonstration, we just simulate agent execution
        # In a real system, this would call the tool in AGENT_REGISTRY
        result = f"Agent '{agent_name}' executed for: {state['messages'][-1].content}"
        return {"results": {agent_name: result}}

    def _build_graph(self):
        """Constructs the LangGraph workflow."""
        self.workflow.add_node("classify", self._classify_intent)
        self.workflow.add_node("execute", self._execute_agent)
        
        self.workflow.set_entry_point("classify")
        self.workflow.add_edge("classify", "execute")
        self.workflow.add_edge("execute", END)
        
        self.graph = self.workflow.compile()

    def run(self, user_input: str) -> str:
        """Runs the orchestrator on user input."""
        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            "intent": "",
            "next_agent": "",
            "results": {}
        }
        final_state = self.graph.invoke(initial_state)
        return str(final_state["results"])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    orchestrator = Orchestrator()
    print(orchestrator.run("Show me the files in the current directory"))
