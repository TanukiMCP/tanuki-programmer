"""
Core Components for Tanuki-PyCharm Architecture

This package contains the foundational base classes, interfaces, and core
infrastructure components for the Tanuki-PyCharm system.
"""

from .base import (
    LayerType,
    AgentType,
    LayerMessage,
    BaseLayer,
    BaseAgent,
    LayerProtocol,
    LoRAAdapterManager,
    SystemConfig
)

__all__ = [
    "LayerType",
    "AgentType", 
    "LayerMessage",
    "BaseLayer",
    "BaseAgent",
    "LayerProtocol",
    "LoRAAdapterManager",
    "SystemConfig"
] 