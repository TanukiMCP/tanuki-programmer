# Tanuki-PyCharm: Domain-Specialized MoA for PyCharm Development (V1.0)

## Executive Summary

Tanuki-PyCharm is a specialized Mixture-of-Agents (MoA) system designed specifically for PyCharm development environments. The system combines 127 specialized expert agents within a unified Python development intelligence framework, leveraging the pure cognitive layer approach and advanced architectural patterns to deliver SOTA performance on consumer hardware while integrating seamlessly with the Cascade PyCharm plugin.

**Key Features:**
- **127 Specialized Expert Agents** optimized for Python and PyCharm workflows
- **Foresight & Adversarial Review** architecture for robust solution generation  
- **Dynamic LoRA Adapter Hotswapping** for efficient resource management
- **128k Context Window** enabling comprehensive briefing packets
- **Zero-Cost Training Data** from Python-focused open-source datasets
- **Pure Cognitive Layer Design** that integrates with any tool-providing environment
- **Optimized Hardware Utilization** (7.5GB VRAM + 25GB RAM from 48GB total)

---

## Table of Contents

1. [Domain Vision & Scope](#1-domain-vision--scope)
2. [System Architecture](#2-system-architecture)
3. [Training Methodology & Datasets](#3-training-methodology--datasets)
4. [Host Environment Integration](#4-host-environment-integration)
5. [Performance, Verification & Quality Assurance](#5-performance-verification--quality-assurance)
6. [Implementation Task List](#6-implementation-task-list)
7. [Packaging & Deployment](#7-packaging--deployment)

---

## 1. Domain Vision & Scope

### 1.1 Core Mission

Tanuki-PyCharm transforms Python development within PyCharm through intelligent automation across the entire development lifecycle. The system provides expert-level capabilities in Python code generation, debugging, testing, refactoring, and project management while maintaining the efficiency and cost-effectiveness needed for widespread adoption in PyCharm environments.

### 1.2 Target Users
- **Python Developers** (junior to senior level using PyCharm)
- **Data Scientists** working with Jupyter, pandas, and ML frameworks
- **Backend Engineers** building APIs and microservices
- **DevOps Engineers** managing Python deployments
- **Research Engineers** prototyping and experimenting

### 1.3 PyCharm-Specialized Expert Agents

The system encompasses 127 specialized agents optimized for PyCharm workflows:

#### Core Python Development Agents
| Agent | Primary Capabilities |
|:---|:---|
| `tanuki-python-planner-critic` | **(Foresight Agent)** Generates and critiques multiple solution paths for Python development |
| `tanuki-python-coder` | Advanced Python code generation with PyCharm project understanding |
| `tanuki-python-reviewer` | Static analysis, code quality assessment, Python best practices |
| `tanuki-python-debugger` | Error diagnosis, stack trace analysis, PyCharm debugger integration |
| `tanuki-python-tester` | pytest, unittest, and comprehensive test generation |
| `tanuki-python-code-reviewer` | **(Adversarial Agent)** Finds logical flaws and edge cases in Python code |

#### Data Science & ML Agents
| Agent | Primary Capabilities |
|:---|:---|
| `tanuki-jupyter` | Jupyter notebook development and cell management |
| `tanuki-pandas` | DataFrame operations and data manipulation |
| `tanuki-numpy` | Numerical computing and array operations |
| `tanuki-sklearn` | Machine learning model development |
| `tanuki-matplotlib` | Data visualization and plotting |
| `tanuki-tensorflow` | Deep learning model development |
| `tanuki-pytorch` | PyTorch model development and training |
| `tanuki-scipy` | Scientific computing and optimization |
| `tanuki-statsmodels` | Statistical modeling and analysis |

#### Web Development & API Agents
| Agent | Primary Capabilities |
|:---|:---|
| `tanuki-django` | Django project management and development |
| `tanuki-flask` | Flask application development |
| `tanuki-fastapi` | FastAPI development and documentation |
| `tanuki-sqlalchemy` | Database ORM and query optimization |
| `tanuki-celery` | Asynchronous task management |
| `tanuki-rest-api` | REST API design and implementation |
| `tanuki-graphql` | GraphQL schema and resolver development |

#### DevOps & Deployment Agents
| Agent | Primary Capabilities |
|:---|:---|
| `tanuki-docker-python` | Python containerization and deployment |
| `tanuki-pip` | Package management and dependency resolution |
| `tanuki-conda` | Conda environment management |
| `tanuki-poetry` | Poetry dependency management |
| `tanuki-pytest-advanced` | Advanced testing strategies and fixtures |
| `tanuki-ci-cd` | Continuous integration and deployment |
| `tanuki-aws-python` | AWS deployment and cloud services |

#### Specialized Python Agents
| Agent | Primary Capabilities |
|:---|:---|
| `tanuki-async-python` | Asynchronous programming patterns |
| `tanuki-python-performance` | Performance optimization and profiling |
| `tanuki-python-security` | Security analysis and vulnerability detection |
| `tanuki-python-packaging` | Package creation and distribution |
| `tanuki-python-typing` | Type hints and static type checking |
| `tanuki-python-docs` | Documentation generation and maintenance |
| `tanuki-python-refactor` | Code refactoring and modernization |

A complete and exhaustive list of all 127 agents, their specific roles, the datasets used for their training, and the knowledge distillation strategy is detailed in **Section 3.4: Comprehensive Adapter Dataset & Distillation Plan**.

---

## 2. System Architecture

### 2.1 The "Brain and Brawn" Philosophy: Pure Cognitive Layer Design

The fundamental design principle of Tanuki-PyCharm follows the pure cognitive layer approach from the Tanuki-Programmer architecture. Our system is designed as a **pure cognitive layer**—a team of expert agents that think, plan, and delegate, but do not execute actions themselves.

-   **The Brain (Our Agent Team)**: The role of our 127 specialized agents is purely cognitive. They analyze Python development problems, formulate multi-step plans, decide which tools to use, and interpret the results of tool execution. Our agents are **tool-aware** (they understand how to use tools like `read_file`, `write_file`, `run_terminal_cmd`) but **tool-agnostic** (they don't care which specific implementation provides these capabilities).

-   **The Brawn (Host Environment Tools)**: The role of tool execution belongs to the host environment—the Cascade PyCharm plugin, MCP servers, or any other tool-providing system. Our agents request tool usage through the standard API, and the host environment handles the actual execution and returns the results.

This separation makes our system:
- **Portable**: Works with any tool-providing environment (Cascade plugin, other IDE extensions, web interfaces)
- **Focused**: Pure cognitive intelligence without execution infrastructure concerns  
- **Compatible**: Leverages existing tool ecosystems rather than replacing them
- **Lightweight**: No tool infrastructure to maintain or deploy

This also clarifies the distinction between our **Mixture-of-Agents (MoA)** architecture and a **Mixture-of-Experts (MoE)** model:
-   An **MoE** is a single model with specialized internal parts (one brain, different lobes).
-   Our **MoA** is a system of multiple specialized agents that uses a team approach (many specialist brains, leveraging external tools).

### 2.2 Multi-Layer Architecture Overview

The system employs a five-layer architecture designed for foresight, execution, and adversarial review:

```
[Host Environment with Tools (e.g., Cascade PyCharm Plugin)]
     |
     v
[Layer 1: Ingress & Sanitizer]───┐
     |                           |
     v                           v
[Layer 2: Foresight Agent]  [Resource Monitor]
     |                           |
     v                           |
[Plan Selection]                 |
     |                           |
     v                           |
[Layer 3: Orchestrator]──────────┘
     |
+----|-------------------------------------------------------------------+
|    v                   Layer 4: Execution & Adversarial Review        |
| [Agent Router]─┬─>[tanuki-python-coder]                               |
|                ├─>[tanuki-django]                                     |
|                ├─>[tanuki-pandas]─┐                                   |
|                └─>[...other agents] |                                 |
|                          |          |                                 |
|                          v          v                                 |
|                 [tanuki-python-code-reviewer]                         |
|                          |                                            |
|                 [Tool Requests]──────────────────────────────────────>┐
+-----------------------------------------------------------------------|
                             |                                          |
                             v                                          |
                    [Host Environment Execution]                        |
                             |                                          |
                             v                                          |
                      [Layer 5: Response Aggregator]                    |
                             |                                          |
                      [Final Python Development Solution]◄──────────────┘
```

### 2.3 Architectural Layers

| Layer | Component | Function |
|:---|:---|:---|
| **1** | **Ingress & Sanitizer** | Input cleaning, normalization, and security validation |
| **2** | **Foresight Agent** | Multi-path planning, strategy critique, and optimal path selection for Python development |
| **3** | **Orchestrator** | Context assembly, briefing packet creation, and expert routing |
| **4** | **Execution & Review** | Expert solution generation with adversarial review loops and tool request coordination |
| **5** | **Response Aggregator** | Solution formatting, final validation, and user delivery |

### 2.4 Dynamic Specialization: Backbone & Adapters

The core efficiency comes from the backbone model architecture with hotswappable specialization:

#### Backbone Model
- **Base Model**: DeepSeek-Coder-V2-Lite (16B) with 128k context window
- **Architecture**: Advanced transformer with RoPE, SwiGLU, and Grouped-Query Attention
- **Parameters**: 16B total
- **Quantization**: IQ4_XS GGUF for balanced performance and VRAM efficiency
- **Memory Usage**: ~7.5GB VRAM (leaving a healthy ~0.5GB buffer for system stability)
- **Specialization**: Fine-tuned on Python-heavy datasets for enhanced Python understanding
- **Always Active**: Provides state-of-the-art Python code intelligence and reasoning

#### LoRA Adapter System
- **127 Specialized Adapters**: Comprehensive Python and PyCharm workflow coverage (~160MB each, scaled for 16B base)
- **Instantaneous Switching**: All 127 adapters are pre-loaded into system RAM
- **System RAM Usage**: ~20.3GB for the adapter pool (127 × 160MB, from 48GB total), eliminating all loading latency
- **PyCharm-Aware**: Each adapter understands PyCharm project structures and development patterns

### 2.5 Context Management & Briefing Packets

The 128k context window enables comprehensive briefing packets for each expert:

```
<PYCHARM_CONTEXT>
  <CONVERSATION_HISTORY>
    <!-- Complete user-AI dialogue -->
  </CONVERSATION_HISTORY>

  <PROJECT_STRUCTURE>
    <!-- Complete Python project structure -->
  </PROJECT_STRUCTURE>

  <RELEVANT_FILES>
    <!-- Full content of Python project files -->
  </RELEVANT_FILES>

  <PYTHON_ENVIRONMENT>
    <!-- Virtual environment, dependencies, interpreter info -->
  </PYTHON_ENVIRONMENT>

  <AVAILABLE_TOOLS>
    <!-- Tool schemas provided by host environment -->
  </AVAILABLE_TOOLS>
  
  <FEW_SHOT_EXAMPLES>
    <!-- Python and PyCharm-specific examples -->
  </FEW_SHOT_EXAMPLES>

  <USER_QUERY>
    <!-- Current specific request -->
  </USER_QUERY>
</PYCHARM_CONTEXT>
```

### 2.6 Resource Management System

Sophisticated resource management ensures efficient operation:

```python
def load_python_adapter(agent_type: str):
    """Instantly switches the active adapter, as all are pre-loaded in RAM."""
    # No dynamic loading needed. Adapters are already in memory.
    # The 'load_lora_weights' function now just points to the active adapter.
    set_active_adapter(f"adapters/tanuki-pycharm/{agent_type}.safetensors")
    update_system_prompt(get_python_agent_instructions(agent_type))
    
    # Performance: <1ms switch time as it's a simple pointer change.

def unload_lru_adapter():
    """No longer needed. All adapters are persistently loaded."""
    pass
```

### 2.7 Architectural Solutions for Complex Python Development

To transition from succeeding at self-contained benchmarks to performing reliably on complex, multi-file Python projects, the architecture employs four key strategies:

#### 1. Countering Architectural Blindness with a Dynamic World Model

-   **Problem**: LLMs lack a persistent "mental model" of the entire Python codebase.
-   **Solution**: The **Orchestrator** builds and maintains a **Dynamic World Model** for Python projects.
    -   **Static Analysis**: The `tanuki-python-architect` analyzes Python project structure, imports, and dependencies
    -   **Dynamic Context**: Maps critical Python files, classes, and functions into the context window
    -   **State Updates**: Tool execution outputs are appended to ensure agents work with ground truth

#### 2. Countering Brittle Planning with a Hierarchical, Iterative Loop

-   **Problem**: LLMs struggle to adapt multi-step Python development plans when errors occur.
-   **Solution**: **Hierarchical & Iterative Planning Loop** for Python development.
    1.  **High-Level Plan (Foresight)**: `tanuki-python-planner-critic` creates strategic plans
    2.  **Sub-Task Execution**: Break down into executable Python development sub-tasks
    3.  **Verification & Update**: Verify each step and adapt based on Python tool feedback
    4.  **Iterate**: Ensure system is in known good state before proceeding

#### 3. Countering Poor Self-Correction with a Mandatory Adversarial Loop

-   **Problem**: An LLM cannot reliably find flaws in its own Python code.
-   **Solution**: **Mandatory Adversarial Loop** for Python development.
    -   **Generation**: `tanuki-python-coder` generates the Python code
    -   **Adversarial Review**: `tanuki-python-code-reviewer` finds logical flaws and edge cases
    -   **Testing**: `tanuki-python-tester` generates comprehensive tests
    -   **Correction Cycle**: Original agent fixes issues based on peer feedback

#### 4. Countering Hallucination with Host Environment Grounding

-   **Problem**: LLMs often hallucinate tool outputs in Python development.
-   **Solution**: The **Host Environment** (Cascade plugin) serves as grounding mechanism.
    -   **Execution Bridge**: Plugin handles actual Python tool execution
    -   **Forced Reality Check**: Real `stdout`, `stderr`, and `exit_code` from Python tools
    -   **Error Propagation**: Real Python errors force agents to confront consequences

---

## 3. Training Methodology & Datasets

### 3.1 Zero-Cost Foundation Training

All foundation training leverages free, open-source datasets from Hugging Face, focused on Python development:

| Expert Agent | Primary Dataset | Synthesis Strategy |
|:---|:---|:---|
| `tanuki-python-coder` | `bigcode/the-stack-v2` (Python subset) | Python code generation with PyCharm context |
| `tanuki-python-reviewer` | `bigcode/starcoderdata` (Python PRs) | Python code review and quality assessment |
| `tanuki-python-debugger` | `microsoft/CodeXGLUE` (Python bugs) | Python bug-fixing scenarios |
| `tanuki-python-tester` | `JetBrains-Research/test-generation` | Python test generation and coverage |
| `tanuki-django` | Django project repositories | Django development patterns |
| `tanuki-pandas` | Kaggle datasets and notebooks | Data manipulation and analysis |
| `tanuki-jupyter` | Jupyter notebook repositories | Interactive Python development |
| `tanuki-fastapi` | FastAPI project repositories | Modern Python API development |

### 3.2 Training Strategy: Distillation from a Peer-Expert Teacher

#### 1. Guiding Philosophy: Specialization through Distillation
Our strategy creates highly specialized Python development agents by fine-tuning, not training from scratch. We employ **knowledge distillation** using a powerful teacher model to generate high-quality examples of ideal Python development behavior.

This approach organizes development into two streams:
1.  **Prompt Engineering (The Teacher's Curriculum):** Defining Python development tasks via PyCharm-specific prompts
2.  **Fine-Tuning (The Student's Study Session):** Training LoRA adapters on teacher-generated Python development data

#### 2. The Models: Teacher vs. Student

**Teacher Model: `deepseek-ai/DeepSeek-Coder-V2-Instruct`**
-   **Role**: Generates synthetic Python development training data
-   **Enhancement**: PyCharm-specific prompts and Python development context
-   **Execution**: Run on GCP cloud VM to generate datasets

**Student Backbone: `deepseek-ai/DeepSeek-Coder-V2-Lite`**
-   **Role**: Foundational engine for Tanuki-PyCharm application
-   **Specialization**: Python development with PyCharm integration understanding

#### 3. The Distillation Workflow

For each of the 127 Python-specialized agents:

1.  **Define Python Agent Task**: Create synthesis prompts for Python development scenarios
2.  **Generate Synthetic Dataset**: Teacher model generates Python development examples with tool usage
3.  **Fine-Tune Student Adapter**: Train LoRA adapter on synthetic Python development data

#### 4. Zero-Cost Execution Plan

-   **Compute (GCP)**: $300 GCP credits for training all 127 Python-specialized adapters
-   **Storage (Local)**: 1TB SSD for Python-focused datasets

### 3.3 Data Synthesis Example for Python Development

```python
def synthesize_python_development_data(python_code_from_stack):
    return {
        "instruction": f"Implement Python function: {extract_docstring(python_code_from_stack)}",
        "thought": "I need to analyze the Python requirements, write clean code, and validate it using Python tools.",
        "tool_calls": [
            {"tool": "write_file", "content": python_code_from_stack, "path": "src/solution.py"},
            {"tool": "run_terminal_cmd", "command": "python -m py_compile src/solution.py"},
            {"tool": "run_terminal_cmd", "command": "python -m pytest tests/test_solution.py"}
        ],
        "final_answer": python_code_from_stack
    }
```

---

## 4. Host Environment Integration

### 4.1 Tool-Agnostic Design Philosophy

Our Python development agents are designed to be **tool-aware** but **tool-agnostic**. They understand Python development tools and PyCharm capabilities but do not contain implementations. Instead, they request tool usage through the host environment's API.

This design provides several key advantages:
- **Compatibility**: Works with Cascade PyCharm plugin and other environments
- **Extensibility**: Automatically gains access to new Python tools
- **Maintainability**: No tool infrastructure to build or maintain
- **Standards Compliance**: Leverages existing Python development ecosystems

### 4.2 Common Python Development Tool Categories

Our agents understand and utilize these Python development tools:

| Tool Category | Examples | Agent Usage |
|:---|:---|:---|
| **File Operations** | `read_file`, `write_file`, `list_files` | Reading Python project context, generating/modifying code |
| **Python Execution** | `run_terminal_cmd`, `python -m` | Running Python scripts, tests, linters, package managers |
| **Code Analysis** | `codebase_search`, `find_references` | Understanding Python project structure and dependencies |
| **Python Tools** | `pylint`, `black`, `mypy`, `pytest` | Code quality, formatting, type checking, testing |
| **Version Control** | Git operations, diff tools | Python project change tracking and collaboration |
| **Package Management** | `pip`, `conda`, `poetry` | Python dependency management and virtual environments |

### 4.3 PyCharm-Specific Integration

The system integrates with PyCharm through the Cascade plugin:

- **Project Context**: Understanding PyCharm project structure and configuration
- **Virtual Environments**: Working with PyCharm's Python interpreter settings
- **Testing Integration**: Leveraging PyCharm's test runner capabilities
- **Debugging Support**: Understanding PyCharm's debugging context and breakpoints
- **Refactoring Tools**: Requesting PyCharm's built-in refactoring operations

---

## 5. Performance, Verification & Quality Assurance

### 5.1 Performance & Efficiency Targets

| Metric | Target | Notes |
|:---|:---|:---|
| **Python Code Generation Accuracy** | 97% on Python-specific benchmarks | Enhanced with PyCharm context understanding |
| **Bug Detection Rate** | 90% on Python Defects4J | Goal for `tanuki-python-debugger` agent |
| **Automated Test Coverage** | 88% line coverage | Goal for `tanuki-python-tester` agent |
| **Simple Function Latency** | < 1.5 seconds | Target for typical Python development tasks |
| **VRAM Usage** | ≤ 7.5 GB | Key hardware constraint for system stability |
| **System RAM Usage (Peak)** | ≤ 25 GB | Target for all adapters loaded plus context cache |
| **Adapter Load Time** | < 1ms | Expected performance due to pre-loading |

### 5.2 Verification Benchmark Suite

| Benchmark Type | Suite / Method | Purpose |
|:---|:---|:---|
| **Standard Benchmarks** | HumanEval+ (Python), Python Defects4J | Industry-standard validation for Python development |
| **PyCharm Integration** | Real PyCharm projects, Django applications | Test PyCharm-specific development workflows |
| **Python Frameworks** | Django, Flask, FastAPI test suites | Validate framework-specific agent capabilities |
| **Data Science** | Kaggle competitions, Jupyter notebooks | Test data science and ML development agents |

### 5.3 User Acceptance Testing (UAT) Plan

| User Persona | Role | Key Tasks | Success Criteria |
|:---|:---|:---|:---|
| **Python Developer** | 2-5 years experience | - Implement Python feature<br>- Debug Python application<br>- Write comprehensive tests | - Accelerates Python development<br>- Provides accurate solutions<br>- Integrates with PyCharm workflow |
| **Data Scientist** | Python + ML focus | - Analyze dataset with pandas<br>- Build ML model<br>- Create Jupyter notebook | - Generates working data science code<br>- Understands ML workflows<br>- Provides statistical insights |
| **Backend Engineer** | API development | - Build FastAPI application<br>- Design database schema<br>- Implement authentication | - Creates production-ready APIs<br>- Follows Python best practices<br>- Handles complex architectures |

---

## 6. Implementation Task List

### Phase 1: Core Infrastructure & Python Agents
*Objective: Build the core MoA platform and train Python development agents.*
- [ ] **GCP Environment Setup**: Configure training infrastructure
- [ ] **Backbone Model Server**: Deploy DeepSeek-Coder-V2-Lite with Python specialization
- [ ] **Resource Manager**: Implement LoRA adapter pre-loading for Python agents
- [ ] **Python Data Pipeline**: Process Python-focused datasets for agent training
- [ ] **Core Python Agent Training**: Fine-tune adapters for core Python development
- [ ] **Initial Benchmarking**: Test Python agents on HumanEval+ and Python-specific benchmarks

### Phase 2: Full-Scale Training & MoA Integration
*Objective: Train all 127 Python-specialized adapters and integrate MoA system.*
- [ ] **Full Python Data Pipeline**: Support all 127 Python agent datasets
- [ ] **Massive-Scale Adapter Training**: Train all Python-specialized LoRA adapters
- [ ] **Orchestrator & Agent Router**: Implement MoA routing for Python development tasks
- [ ] **Foresight & Review Implementation**: Build Python-specific planning and review agents
- [ ] **Host Environment API**: Standardized API for Cascade plugin integration
- [ ] **Full Integration Testing**: Test multi-agent Python development workflows

### Phase 3: Deployment & Finalization
*Objective: Package and deploy the complete Python MoA system.*
- [ ] **Packaging & Distribution**: Docker Compose setup for local deployment
- [ ] **Cascade Plugin Integration**: Test with actual Cascade PyCharm plugin
- [ ] **User Acceptance Testing**: Execute UAT with Python developers
- [ ] **Final Documentation**: Comprehensive setup and usage guides

---

## 7. Packaging & Deployment

### 7.1 Local Deployment: Pure Cognitive Layer

Tanuki-PyCharm is designed as a pure cognitive layer that integrates with the Cascade PyCharm plugin. The system requires no built-in tool infrastructure, making deployment lightweight and focused.

The system will be packaged using **Docker Compose** for simple deployment:

1.  **Inference Server (`vLLM`)**:
    *   Serves the `DeepSeek-Coder-V2-Lite` base model
    *   Loads all 127 Python-specialized LoRA adapters simultaneously
    *   Applies different adapters per request for MoA functionality

2.  **Orchestrator Service**:
    *   Implements the MoA cognitive system
    *   Manages Dynamic World Model for Python projects
    *   Routes requests to appropriate Python development agents
    *   Coordinates tool requests back to Cascade plugin

### 7.2 Cascade PyCharm Plugin Integration

The system integrates with PyCharm through the Cascade plugin:

#### Step 1: Run the Local Tanuki-PyCharm Server

```bash
docker-compose up tanuki-pycharm
```

#### Step 2: Configure Cascade Plugin

1. **Navigate to PyCharm Settings**: Tools > Cascade
2. **Set Custom Model Provider**: 
   - Model Name: `tanuki-pycharm`
   - API Base URL: `http://localhost:8000/v1`
3. **Start Python Development**: All Cascade interactions now powered by Tanuki-PyCharm

### 7.3 Future of AI in Python Development

Tanuki-PyCharm represents the future of AI in Python development:

**Superintelligence in Python Development:**
- **Context-Aware Python Intelligence**: Understanding full Python project context
- **Adaptive Learning**: Learning from Python development patterns and feedback
- **Predictive Assistance**: Anticipating Python developer needs
- **Collaborative Intelligence**: Amplifying Python developer capabilities

**Resource Management Excellence:**
- **Efficient Context Utilization**: Maximizing 128k context for Python projects
- **Dynamic Adaptation**: Adjusting strategies based on Python project complexity
- **Python Tool Integration**: Seamlessly coordinating Python development tools
- **Performance Optimization**: Balancing intelligence with responsiveness

*Domain: Python Development in PyCharm | Target Users: Python Developers, Data Scientists, Backend Engineers*
*Last Updated: January 2025 | Version: 1.0 | Status: Implementation Blueprint* 