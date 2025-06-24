"""
Agent Implementations for Tanuki-PyCharm

This package contains the 127 specialized expert agents organized by category:
- core_python: Core Python development agents (15)
- data_science: Data science and ML agents (25)  
- web_development: Web development and API agents (22)
- devops: DevOps and deployment agents (15)
- specialized: Specialized domain agents (50)
"""

from .core_python import *
from .data_science import *
from .web_development import *
from .devops import *
from .specialized import *

__all__ = [
    # Core Python agents will be imported from submodules
] 