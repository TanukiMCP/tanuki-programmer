"""
Tanuki Python Debugger Agent

Specialized agent for Python debugging and error resolution.
"""

from typing import Dict, Any, List, Optional
from src.core.base import BaseAgent, AgentType


class TanukiPythonDebugger(BaseAgent):
    """Expert agent for Python debugging and error resolution."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(
            agent_name="tanuki-python-debugger",
            agent_type=AgentType.CORE_PYTHON,
            config=config or {}
        )
        
    def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute debugging task."""
        return {
            "status": "completed",
            "agent": self.agent_name,
            "output": f"Debugging task: {task.get('description', 'No description')}"
        }
    
    def get_capabilities(self) -> List[str]:
        return ["debugging", "error_analysis", "performance_analysis"]
    
    def get_required_tools(self) -> List[str]:
        return ["read_file", "run_debugger", "analyze_logs"] 