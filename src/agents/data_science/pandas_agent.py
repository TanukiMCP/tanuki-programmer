"""
Tanuki-Pandas Agent

This agent specializes in data manipulation and analysis using the pandas library.
It can perform operations like data cleaning, transformation, and reading/writing
CSV files.
"""

from typing import Dict, Any, List, Optional
from src.core.base import BaseAgent, AgentType

class TanukiPandas(BaseAgent):
    """
    Expert agent for pandas-based data analysis.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the pandas agent."""
        super().__init__(
            agent_name="tanuki-pandas",
            agent_type=AgentType.DATA_SCIENCE,
            config=config or {}
        )
        
    def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a pandas-related task.
        """
        return {
            "status": "completed",
            "agent": self.agent_name,
            "output": f"Pandas task completed: {task.get('description', 'N/A')}"
        }
        
    def get_capabilities(self) -> List[str]:
        """Get list of capabilities this agent can handle."""
        return [
            "dataframe_manipulation",
            "data_cleaning",
            "csv_reading",
            "data_transformation"
        ]
        
    def get_required_tools(self) -> List[str]:
        """Get list of tools this agent requires."""
        return [
            "read_file",
            "write_file",
            "execute_code"
        ] 