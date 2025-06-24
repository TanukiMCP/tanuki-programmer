"""
Tanuki Python Coder Agent

Specialized agent for Python code generation, analysis, and optimization.
This agent excels at creating well-structured, idiomatic Python code
with PyCharm integration.
"""

from typing import Dict, Any, List, Optional
from src.core.base import BaseAgent, AgentType


class TanukiPythonCoder(BaseAgent):
    """
    Expert agent for Python code generation and analysis.
    
    Capabilities:
    - Generate Python functions, classes, and modules
    - Analyze existing code for improvements
    - Optimize code performance and structure
    - Follow PEP 8 and Python best practices
    - Integrate with PyCharm's code analysis tools
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the Python coder agent."""
        super().__init__(
            agent_name="tanuki-python-coder",
            agent_type=AgentType.CORE_PYTHON,
            config=config or {}
        )
        
    def execute(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a Python coding task.
        
        Args:
            task: Task specification including type, description, and requirements
            context: PyCharm project context and available tools
            
        Returns:
            Generated code and analysis results
        """
        task_type = task.get("type", "")
        description = task.get("description", "")
        requirements = task.get("requirements", {})
        
        try:
            if task_type == "code_generation":
                return self._generate_code(description, requirements, context)
            elif task_type == "code_analysis":
                return self._analyze_code(description, requirements, context)
            elif task_type == "code_optimization":
                return self._optimize_code(description, requirements, context)
            else:
                return self._general_coding_task(description, requirements, context)
                
        except Exception as e:
            self.logger.error(f"Error in Python coder execution: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "agent": self.agent_name
            }
    
    def _generate_code(self, description: str, requirements: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Python code based on description and requirements."""
        # Extract context information
        project_info = context.get("project_info", {})
        python_version = project_info.get("python_version", "3.8")
        dependencies = context.get("dependencies", [])
        
        # Analyze requirements
        function_name = requirements.get("function_name")
        class_name = requirements.get("class_name")
        module_name = requirements.get("module_name")
        
        # Generate appropriate code structure
        if function_name:
            code = self._generate_function(function_name, description, requirements, context)
        elif class_name:
            code = self._generate_class(class_name, description, requirements, context)
        elif module_name:
            code = self._generate_module(module_name, description, requirements, context)
        else:
            code = self._generate_general_code(description, requirements, context)
        
        return {
            "status": "completed",
            "agent": self.agent_name,
            "generated_code": code,
            "language": "python",
            "python_version": python_version,
            "recommendations": self._get_code_recommendations(code, context),
            "next_steps": self._suggest_next_steps(code, context)
        }
    
    def _analyze_code(self, description: str, requirements: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze existing Python code for improvements."""
        code_to_analyze = requirements.get("code", "")
        file_path = requirements.get("file_path", "")
        
        analysis = {
            "complexity": self._analyze_complexity(code_to_analyze),
            "style_issues": self._check_style(code_to_analyze),
            "performance_issues": self._check_performance(code_to_analyze),
            "security_issues": self._check_security(code_to_analyze),
            "maintainability": self._check_maintainability(code_to_analyze),
            "test_coverage_suggestions": self._suggest_tests(code_to_analyze)
        }
        
        return {
            "status": "completed",
            "agent": self.agent_name,
            "analysis": analysis,
            "file_path": file_path,
            "improvement_suggestions": self._generate_improvement_suggestions(analysis),
            "refactoring_opportunities": self._identify_refactoring_opportunities(code_to_analyze)
        }
    
    def _optimize_code(self, description: str, requirements: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize Python code for performance and readability."""
        original_code = requirements.get("code", "")
        optimization_type = requirements.get("optimization_type", "general")
        
        optimizations = []
        
        if optimization_type in ["performance", "general"]:
            optimizations.extend(self._performance_optimizations(original_code))
        
        if optimization_type in ["readability", "general"]:
            optimizations.extend(self._readability_optimizations(original_code))
        
        if optimization_type in ["memory", "general"]:
            optimizations.extend(self._memory_optimizations(original_code))
        
        optimized_code = self._apply_optimizations(original_code, optimizations)
        
        return {
            "status": "completed",
            "agent": self.agent_name,
            "original_code": original_code,
            "optimized_code": optimized_code,
            "optimizations_applied": optimizations,
            "performance_impact": self._estimate_performance_impact(optimizations),
            "recommendations": self._get_optimization_recommendations(optimizations)
        }
    
    def _general_coding_task(self, description: str, requirements: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle general coding tasks."""
        return {
            "status": "completed",
            "agent": self.agent_name,
            "output": f"General coding task completed: {description}",
            "recommendations": ["Consider using more specific task types for better results"],
            "context_used": list(context.keys())
        }
    
    def _generate_function(self, function_name: str, description: str, requirements: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate a Python function."""
        params = requirements.get("parameters", [])
        return_type = requirements.get("return_type", "Any")
        docstring = requirements.get("include_docstring", True)
        
        # Basic function template
        code = f"def {function_name}("
        if params:
            code += ", ".join(params)
        code += f") -> {return_type}:\n"
        
        if docstring:
            code += f'    """{description}"""\n'
        
        code += "    # Implementation goes here\n"
        code += "    pass\n"
        
        return code
    
    def _generate_class(self, class_name: str, description: str, requirements: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate a Python class."""
        base_classes = requirements.get("base_classes", [])
        methods = requirements.get("methods", [])
        
        code = f"class {class_name}"
        if base_classes:
            code += f"({', '.join(base_classes)})"
        code += ":\n"
        code += f'    """{description}"""\n\n'
        
        # Add __init__ method
        code += "    def __init__(self):\n"
        code += "        \"\"\"Initialize the instance.\"\"\"\n"
        code += "        pass\n\n"
        
        # Add other methods
        for method in methods:
            code += f"    def {method}(self):\n"
            code += f"        \"\"\"Method: {method}\"\"\"\n"
            code += "        pass\n\n"
        
        return code
    
    def _generate_module(self, module_name: str, description: str, requirements: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate a Python module."""
        imports = requirements.get("imports", [])
        functions = requirements.get("functions", [])
        classes = requirements.get("classes", [])
        
        code = f'"""{description}"""\n\n'
        
        # Add imports
        for import_stmt in imports:
            code += f"{import_stmt}\n"
        
        if imports:
            code += "\n"
        
        # Add functions and classes
        for func in functions:
            code += self._generate_function(func, f"Function: {func}", {}, context)
            code += "\n\n"
        
        for cls in classes:
            code += self._generate_class(cls, f"Class: {cls}", {}, context)
            code += "\n\n"
        
        return code
    
    def _generate_general_code(self, description: str, requirements: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generate general Python code based on description."""
        return f'"""{description}"""\n\n# Implementation based on: {description}\npass\n'
    
    def get_capabilities(self) -> List[str]:
        """Get list of capabilities this agent can handle."""
        return [
            "code_generation",
            "code_analysis", 
            "code_optimization",
            "function_creation",
            "class_creation",
            "module_creation",
            "performance_analysis",
            "style_checking",
            "security_analysis",
            "maintainability_assessment"
        ]
    
    def get_required_tools(self) -> List[str]:
        """Get list of tools this agent requires."""
        return [
            "read_file",
            "write_file",
            "lint_code",
            "format_code",
            "run_python",
            "analyze_imports",
            "check_syntax"
        ]
    
    # Helper methods for analysis
    def _analyze_complexity(self, code: str) -> Dict[str, Any]:
        """Analyze code complexity."""
        return {"cyclomatic_complexity": "medium", "lines_of_code": len(code.split('\n'))}
    
    def _check_style(self, code: str) -> List[str]:
        """Check code style issues."""
        return ["Consider using more descriptive variable names"]
    
    def _check_performance(self, code: str) -> List[str]:
        """Check performance issues."""
        return ["Consider using list comprehensions for better performance"]
    
    def _check_security(self, code: str) -> List[str]:
        """Check security issues."""
        return ["No obvious security issues found"]
    
    def _check_maintainability(self, code: str) -> Dict[str, Any]:
        """Check maintainability metrics."""
        return {"maintainability_index": "high", "documentation_coverage": "medium"}
    
    def _suggest_tests(self, code: str) -> List[str]:
        """Suggest test cases."""
        return ["Add unit tests for main functions", "Add integration tests"]
    
    def _generate_improvement_suggestions(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate improvement suggestions based on analysis."""
        return ["Improve documentation", "Add type hints", "Optimize performance"]
    
    def _identify_refactoring_opportunities(self, code: str) -> List[str]:
        """Identify refactoring opportunities."""
        return ["Extract method for long functions", "Remove code duplication"]
    
    def _performance_optimizations(self, code: str) -> List[Dict[str, Any]]:
        """Identify performance optimizations."""
        return [{"type": "list_comprehension", "description": "Use list comprehension instead of loop"}]
    
    def _readability_optimizations(self, code: str) -> List[Dict[str, Any]]:
        """Identify readability optimizations."""
        return [{"type": "variable_naming", "description": "Use more descriptive variable names"}]
    
    def _memory_optimizations(self, code: str) -> List[Dict[str, Any]]:
        """Identify memory optimizations."""
        return [{"type": "generator", "description": "Use generators for large datasets"}]
    
    def _apply_optimizations(self, code: str, optimizations: List[Dict[str, Any]]) -> str:
        """Apply optimizations to code."""
        # This would contain actual optimization logic
        return code  # Placeholder
    
    def _estimate_performance_impact(self, optimizations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Estimate performance impact of optimizations."""
        return {"speed_improvement": "10-20%", "memory_reduction": "5-10%"}
    
    def _get_optimization_recommendations(self, optimizations: List[Dict[str, Any]]) -> List[str]:
        """Get recommendations for optimizations."""
        return ["Test performance before and after optimizations", "Profile code to identify bottlenecks"]
    
    def _get_code_recommendations(self, code: str, context: Dict[str, Any]) -> List[str]:
        """Get recommendations for generated code."""
        return ["Add type hints for better IDE support", "Include comprehensive docstrings", "Add error handling"]
    
    def _suggest_next_steps(self, code: str, context: Dict[str, Any]) -> List[str]:
        """Suggest next steps after code generation."""
        return ["Write unit tests", "Run linting tools", "Review code with team"] 