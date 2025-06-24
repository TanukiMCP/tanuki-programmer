"""
Core Base Classes and Interfaces for Tanuki-PyCharm Architecture

This module defines the foundational base classes and interfaces that all layers
and components in the Tanuki-PyCharm system inherit from.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from enum import Enum
import logging
from dataclasses import dataclass


class LayerType(Enum):
    """Types of layers in the 6-layer architecture."""
    CONTEXT_INGESTION = "layer1_context_ingestion"
    PROJECT_UNDERSTANDING = "layer2_project_understanding"
    FORESIGHT_AGENT = "layer3_foresight_agent"
    ORCHESTRATOR_PLANNER = "layer4_orchestrator_planner"
    EXPERT_AGENT_EXECUTION = "layer5_expert_agents"
    RESPONSE_INTEGRATION = "layer6_response_integration"


class AgentType(Enum):
    """Types of expert agents in the system."""
    CORE_PYTHON = "core_python"
    DATA_SCIENCE = "data_science"
    WEB_DEVELOPMENT = "web_development"
    DEVOPS = "devops"
    SPECIALIZED = "specialized"


@dataclass
class LayerMessage:
    """Message structure for inter-layer communication."""
    source_layer: LayerType
    target_layer: LayerType
    message_type: str
    payload: Dict[str, Any]
    timestamp: float
    correlation_id: str


class BaseLayer(ABC):
    """
    Abstract base class for all layers in the 6-layer architecture.
    
    Each layer must implement the process method and can optionally
    override other lifecycle methods.
    """
    
    def __init__(self, layer_type: LayerType, config: Optional[Dict[str, Any]] = None):
        """Initialize the base layer."""
        self.layer_type = layer_type
        self.config = config or {}
        self.logger = logging.getLogger(f"tanuki.{layer_type.value}")
        self._is_initialized = False
        
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process input data and return results.
        
        Args:
            input_data: Input data from previous layer or external source
            
        Returns:
            Processed data to pass to next layer
        """
        pass
    
    def initialize(self) -> None:
        """Initialize the layer. Override in subclasses for custom initialization."""
        self._is_initialized = True
        self.logger.info(f"Layer {self.layer_type.value} initialized")
    
    def cleanup(self) -> None:
        """Cleanup resources. Override in subclasses for custom cleanup."""
        self.logger.info(f"Layer {self.layer_type.value} cleaned up")
    
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data. Override in subclasses for custom validation."""
        return isinstance(input_data, dict)
    
    def get_status(self) -> Dict[str, Any]:
        """Get layer status information."""
        return {
            "layer_type": self.layer_type.value,
            "is_initialized": self._is_initialized,
            "config": self.config
        }


class BaseAgent(ABC):
    """
    Abstract base class for all expert agents in the system.
    
    Each expert agent must implement the execute method and specify
    its capabilities and requirements.
    """
    
    def __init__(self, agent_name: str, agent_type: AgentType, config: Optional[Dict[str, Any]] = None):
        """Initialize the base agent."""
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.config = config or {}
        self.logger = logging.getLogger(f"tanuki.agent.{agent_name}")
        self.lora_adapter_path: Optional[str] = None
        self._is_loaded = False
        
    @abstractmethod
    def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task with the given context.
        
        Args:
            task: Task description and parameters
            context: Execution context from previous layers
            
        Returns:
            Task execution results
        """
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Get list of capabilities this agent can handle.
        
        Returns:
            List of capability strings
        """
        pass
    
    @abstractmethod
    def get_required_tools(self) -> List[str]:
        """
        Get list of tools this agent requires.
        
        Returns:
            List of tool names
        """
        pass
    
    def load_adapter(self, adapter_path: str) -> bool:
        """
        Load LoRA adapter for this agent.
        
        Args:
            adapter_path: Path to the LoRA adapter
            
        Returns:
            True if loaded successfully
        """
        self.lora_adapter_path = adapter_path
        self._is_loaded = True
        self.logger.info(f"Loaded LoRA adapter for {self.agent_name}: {adapter_path}")
        return True
    
    def unload_adapter(self) -> bool:
        """
        Unload LoRA adapter for this agent.
        
        Returns:
            True if unloaded successfully
        """
        self.lora_adapter_path = None
        self._is_loaded = False
        self.logger.info(f"Unloaded LoRA adapter for {self.agent_name}")
        return True
    
    def is_loaded(self) -> bool:
        """Check if agent's LoRA adapter is loaded."""
        return self._is_loaded
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status information."""
        return {
            "agent_name": self.agent_name,
            "agent_type": self.agent_type.value,
            "is_loaded": self._is_loaded,
            "adapter_path": self.lora_adapter_path,
            "capabilities": self.get_capabilities(),
            "required_tools": self.get_required_tools()
        }


class LayerProtocol(ABC):
    """
    Protocol for inter-layer communication in the 6-layer architecture.
    """
    
    @abstractmethod
    def send_message(self, message: LayerMessage) -> bool:
        """Send a message to another layer."""
        pass
    
    @abstractmethod
    def receive_message(self, message: LayerMessage) -> Dict[str, Any]:
        """Receive and process a message from another layer."""
        pass


class LoRAAdapterManager:
    """
    Manager for LoRA adapter loading, unloading, and switching.
    
    Handles the dynamic switching between the 127 specialized agents
    by managing their LoRA adapters efficiently.
    """
    
    def __init__(self, adapter_base_path: str = "models/adapters"):
        """Initialize the LoRA adapter manager."""
        self.adapter_base_path = adapter_base_path
        self.loaded_adapters: Dict[str, str] = {}
        self.adapter_cache: Dict[str, Any] = {}
        self.logger = logging.getLogger("tanuki.lora_manager")
        
    def load_adapter(self, agent_name: str, adapter_name: str) -> bool:
        """
        Load a LoRA adapter for the specified agent.
        
        Args:
            agent_name: Name of the agent
            adapter_name: Name of the adapter to load
            
        Returns:
            True if loaded successfully
        """
        adapter_path = f"{self.adapter_base_path}/{adapter_name}"
        self.loaded_adapters[agent_name] = adapter_path
        self.logger.info(f"Loaded adapter {adapter_name} for agent {agent_name}")
        return True
    
    def unload_adapter(self, agent_name: str) -> bool:
        """
        Unload the LoRA adapter for the specified agent.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            True if unloaded successfully
        """
        if agent_name in self.loaded_adapters:
            adapter_path = self.loaded_adapters.pop(agent_name)
            self.logger.info(f"Unloaded adapter for agent {agent_name}: {adapter_path}")
            return True
        return False
    
    def switch_adapter(self, agent_name: str, new_adapter_name: str) -> bool:
        """
        Switch to a different LoRA adapter for the specified agent.
        
        Args:
            agent_name: Name of the agent
            new_adapter_name: Name of the new adapter
            
        Returns:
            True if switched successfully
        """
        self.unload_adapter(agent_name)
        return self.load_adapter(agent_name, new_adapter_name)
    
    def get_loaded_adapters(self) -> Dict[str, str]:
        """Get dictionary of currently loaded adapters."""
        return self.loaded_adapters.copy()
    
    def preload_adapters(self, agent_adapter_map: Dict[str, str]) -> bool:
        """
        Preload multiple adapters for efficient switching.
        
        Args:
            agent_adapter_map: Mapping of agent names to adapter names
            
        Returns:
            True if all adapters loaded successfully
        """
        success = True
        for agent_name, adapter_name in agent_adapter_map.items():
            if not self.load_adapter(agent_name, adapter_name):
                success = False
        return success


class SystemConfig:
    """
    System-wide configuration management for Tanuki-PyCharm.
    
    Manages configuration for all layers, agents, and system components.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize system configuration."""
        self.config_path = config_path
        self.config: Dict[str, Any] = {
            "system": {
                "max_context_length": 128000,
                "max_agents_concurrent": 5,
                "adapter_cache_size": 10,
            },
            "layers": {
                "layer1_context_ingestion": {"enabled": True},
                "layer2_project_understanding": {"enabled": True},
                "layer3_foresight_agent": {"enabled": True},
                "layer4_orchestrator_planner": {"enabled": True},
                "layer5_expert_agents": {"enabled": True},
                "layer6_response_integration": {"enabled": True},
            },
            "agents": {
                "core_python": {"count": 15, "base_adapter": "tanuki-python-base"},
                "data_science": {"count": 25, "base_adapter": "tanuki-datascience-base"},
                "web_development": {"count": 22, "base_adapter": "tanuki-web-base"},
                "devops": {"count": 15, "base_adapter": "tanuki-devops-base"},
                "specialized": {"count": 50, "base_adapter": "tanuki-specialized-base"},
            },
            "pycharm": {
                "integration_enabled": True,
                "context_refresh_interval": 30,
                "tool_timeout": 300,
            }
        }
        
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path to configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> None:
        """
        Set configuration value using dot notation.
        
        Args:
            key_path: Dot-separated path to configuration key
            value: Value to set
        """
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def get_layer_config(self, layer_type: LayerType) -> Dict[str, Any]:
        """Get configuration for a specific layer."""
        return self.get(f"layers.{layer_type.value}", {})
    
    def get_agent_config(self, agent_type: AgentType) -> Dict[str, Any]:
        """Get configuration for a specific agent type."""
        return self.get(f"agents.{agent_type.value}", {}) 