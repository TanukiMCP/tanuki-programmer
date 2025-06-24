"""
Tanuki-PyCharm: Domain-Specialized Mixture-of-Agents for PyCharm Development

A specialized Mixture-of-Agents (MoA) system designed for PyCharm development
environments, featuring 127 specialized expert agents with LoRA adapter swapping
for efficient resource management and superior Python development capabilities.

This is a pure cognitive layer designed for model training and distillation,
not tool execution infrastructure.
"""

from .core.base import BaseAgent, AgentType, LoRAAdapterManager, SystemConfig
from .training.model_training import ModelTrainer
from .training.data_synthesis import DataSynthesisPipeline

__version__ = "1.0.0"
__author__ = "Tanuki-PyCharm Team"

__all__ = [
    # Core MoA components
    "BaseAgent",
    "AgentType", 
    "LoRAAdapterManager",
    "SystemConfig",
    
    # Training pipeline
    "ModelTrainer",
    "DataSynthesisPipeline",
] 