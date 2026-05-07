import subprocess
import logging
from typing import Dict, Any, List
from langchain.tools import tool

logger = logging.getLogger(__name__)

class SpecialistAgent:
    """Base class for ECHOME specialist agents."""
    def __init__(self, name: str):
        self.name = name

class BashAgent(SpecialistAgent):
    """Executes shell commands safely."""
    def __init__(self):
        super().__init__("BashAgent")

    @tool
    def execute_command(self, command: str) -> str:
        """Executes a bash command and returns the output."""
        logger.info(f"Executing bash command: {command}")
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=30
            )
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Error executing command: {str(e)}"

class TechAgent(SpecialistAgent):
    """Answers engineering and architecture questions."""
    def __init__(self):
        super().__init__("TechAgent")

    @tool
    def analyze_architecture(self, context: str) -> str:
        """Analyzes technical architecture based on provided context."""
        # This would typically interface with an LLM
        return f"Analyzing technical context for: {context}"

# Registry of agents
AGENT_REGISTRY = {
    "bash": BashAgent(),
    "tech": TechAgent()
}
