import time
from typing import Dict, Any, List, Optional

class Orchestrator:
    """
    The Orchestrator component (Layer 3) responsible for managing agent workflows.
    It coordinates the flow of tasks between different specialized agents.
    """

    def __init__(self):
        self.agent_router = AgentRouter()
        self.context_manager = ContextManager()
        self.response_aggregator = ResponseAggregator()
        self.workflow_history: List[Dict[str, Any]] = []

    def execute_workflow(self, initial_task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a complete workflow by routing tasks to appropriate agents,
        managing context, and aggregating responses.

        Args:
            initial_task (Dict[str, Any]): The initial task description and data.

        Returns:
            Dict[str, Any]: The final aggregated solution from the workflow.
        """
        print(f"Orchestrator: Starting workflow for task: {initial_task.get('description', 'No description')}")
        self.workflow_history = [] # Reset history for new workflow

        current_task = initial_task
        while True:
            # 1. Prepare briefing packet for the Foresight Agent (or initial routing)
            # Extract tool outputs from the last agent's response, if available
            last_tool_outputs = self.workflow_history[-1].get("response", {}).get("tool_calls") if self.workflow_history else None
            
            briefing_packet = self.context_manager.assemble_briefing_packet(
                conversation_history=self.workflow_history,
                current_task=current_task,
                relevant_files={}, # Placeholder for now, will be populated by ContextManager
                tool_schemas=[],   # Placeholder for now, will be populated by ContextManager
                few_shot_examples=[], # Placeholder for now, will be populated by ContextManager
                last_tool_outputs=last_tool_outputs # Pass tool outputs from previous step
            )

            # 2. Route the task to the appropriate agent
            # In a real scenario, the AgentRouter would interact with a Foresight Agent
            # to determine the next best agent. For now, we'll simulate a simple routing.
            next_agent_name = self.agent_router.route_task(briefing_packet)
            print(f"Orchestrator: Routing task to {next_agent_name}")

            # Dispatch task to the appropriate agent
            agent_response = self._dispatch_agent_task(next_agent_name, briefing_packet)
            self.workflow_history.append({
                "agent": next_agent_name,
                "task": current_task,
                "response": agent_response
            })

            # 3. Check if the workflow is complete or needs further steps
            if agent_response.get("status") == "completed" or not agent_response.get("next_task"):
                print("Orchestrator: Workflow completed.")
                break
            else:
                current_task = agent_response["next_task"]
                print(f"Orchestrator: Continuing with next task: {current_task.get('description', 'No description')}")

        # 4. Aggregate and finalize the solution
        final_solution = self.response_aggregator.aggregate_response(self.workflow_history)
        print("Orchestrator: Final solution aggregated.")
        return final_solution

    def _dispatch_agent_task(self, agent_name: str, briefing_packet: Dict[str, Any]) -> Dict[str, Any]:
        """
        Dispatches the task to the specified agent and retrieves its response.
        In a production system, this would involve calling the actual agent's inference endpoint
        and handling its specific output structure.
        """
        print(f"Orchestrator: Dispatching task to {agent_name} with briefing for: {briefing_packet.get('current_task', {}).get('description')}")
        
        # This method defines the interface for agent execution.
        # The actual agent logic (LLM inference, tool use) will be implemented by
        # the specialized agents in later phases (Phase 2 and 3).
        # For now, we simulate agent responses with basic error handling and retries.

        max_retries = 3
        retry_delay_seconds = 1

        for attempt in range(max_retries):
            try:
                print(f"Orchestrator: Attempt {attempt + 1}/{max_retries} to dispatch task to {agent_name} for: {briefing_packet.get('current_task', {}).get('description')}")
                
                # Simulate different agent behaviors
                if agent_name == "tanuki-code-reviewer":
                    # Simulate review: sometimes requests corrections, sometimes approves
                    task_description = briefing_packet.get('current_task', {}).get('description', '').lower()
                    if "bug" in task_description or "refactor" in task_description:
                        print(f"Orchestrator: {agent_name} requests corrections for: {task_description}")
                        return {
                            "status": "needs_correction",
                            "output": f"Review by {agent_name}: Corrections needed for '{task_description}'. Please address identified issues.",
                            "next_task": {
                                "description": f"Address corrections requested by tanuki-code-reviewer for: {task_description}",
                                "type": "correction",
                                "original_task": briefing_packet.get('current_task')
                            }
                        }
                    else:
                        print(f"Orchestrator: {agent_name} approves task: {task_description}")
                        return {"status": "approved", "output": f"Review by {agent_name}: Approved task '{task_description}'."}
                else:
                    # For other agents, simulate completion
                    # Introduce a simulated failure for demonstration purposes
                    current_task_description = briefing_packet.get('current_task', {}).get('description', '').lower()
                    if "fail_task" in current_task_description and attempt == 0:
                        raise RuntimeError(f"Simulated transient error during {agent_name} execution.")
                    
                    # Simulate tool calls for "coding_with_tools" type tasks
                    tool_calls = []
                    if briefing_packet.get('current_task', {}).get('type') == "coding_with_tools":
                        tool_calls.append({"tool_name": "write_file", "parameters": {"path": "src/temp_file.py", "content": "print('Hello, World!')"}})
                        tool_calls.append({"tool_name": "lint_code", "parameters": {"language": "python", "code": "print('Hello, World!')"}})

                    return {"status": "completed", "output": f"Task processed by {agent_name}.", "tool_calls": tool_calls}

            except Exception as e:
                print(f"Orchestrator: Error dispatching task to {agent_name} (Attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    print(f"Orchestrator: Retrying in {retry_delay_seconds} seconds...")
                    time.sleep(retry_delay_seconds)
                else:
                    print(f"Orchestrator: Max retries reached for {agent_name}. Task failed.")
                    return {"status": "failed", "output": f"Task failed after {max_retries} attempts: {e}"}
        
        # Should not be reached if loop logic is correct, but for type hinting
        return {"status": "failed", "output": "Unexpected error in dispatch logic."}


class AgentRouter:
    """
    The Agent Router dynamically selects and routes tasks to the appropriate
    specialized agent based on the Foresight Agent's plan.
    """
    def route_task(self, briefing_packet: Dict[str, Any]) -> str:
        """
        Determines the next agent to handle the task.
        This implementation uses simple rule-based routing.
        """
        current_task = briefing_packet.get('current_task', {})
        task_description = current_task.get('description', '').lower()
        task_type = current_task.get('type')

        # If it's a correction task, route back to the original agent or a specific correction agent
        if task_type == "correction" and "original_task" in current_task:
            original_task_type = current_task["original_task"].get("type")
            if original_task_type == "coding":
                return "tanuki-coder" # Route back to coder for code corrections
            elif original_task_type == "bug_fix":
                return "tanuki-debugger" # Route back to debugger for bug fix corrections
            # Add more specific routing for other original task types as needed
            print(f"AgentRouter: Routing correction task of type '{original_task_type}' to tanuki-generalist.")
            return "tanuki-generalist" # Fallback for corrections

        # Original routing logic for new tasks
        if "implement" in task_description or "write code" in task_description:
            return "tanuki-coder"
        elif "plan" in task_description or "architect" in task_description:
            return "tanuki-planner-critic"
        elif "fix bug" in task_description or "debug" in task_description:
            return "tanuki-debugger"
        elif "review" in task_description:
            return "tanuki-code-reviewer"
        elif "test" in task_description:
            return "tanuki-tester"
        else:
            return "tanuki-generalist" # Default agent

class ContextManager:
    """
    The Context Manager module to assemble and compress "briefing packets" for agents,
    including conversation history, relevant files, tool schemas, and few-shot examples.
    """
    def assemble_briefing_packet(self,
                                 conversation_history: List[Dict[str, Any]],
                                 current_task: Dict[str, Any],
                                 relevant_files: Dict[str, str],
                                 tool_schemas: List[Dict[str, Any]],
                                 few_shot_examples: List[Dict[str, Any]],
                                 last_tool_outputs: Optional[List[Dict[str, Any]]] = None # New parameter
                                ) -> Dict[str, Any]:
        """
        Assembles a briefing packet for an agent.
        Context compression techniques (e.g., LLMLingua) will be integrated in a later phase.
        """
        print("ContextManager: Assembling briefing packet...")
        briefing = {
            "conversation_history": conversation_history,
            "current_task": current_task,
            "relevant_files": relevant_files,
            "tool_schemas": tool_schemas,
            "few_shot_examples": few_shot_examples,
            "last_tool_outputs": last_tool_outputs, # Include new parameter
            "timestamp": time.time()
        }
        return briefing

class ResponseAggregator:
    """
    The Response Aggregator (Layer 5) to format and finalize solutions from expert agents.
    """
    def aggregate_response(self, workflow_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Aggregates responses from the workflow history into a final solution.
        """
        print("ResponseAggregator: Aggregating responses...")
        final_output = []
        for step in workflow_history:
            agent = step.get("agent", "unknown_agent")
            response_output = step.get("response", {}).get("output", "No output.")
            tool_outputs = step.get("response", {}).get("tool_calls", [])
            
            final_output.append(f"[{agent}]: {response_output}")
            if tool_outputs:
                final_output.append(f"  Tool Outputs: {json.dumps(tool_outputs, indent=2)}")
        
        return {
            "final_solution": "\n".join(final_output),
            "status": "success"
        }

if __name__ == "__main__":
    import json # Import json for pretty printing in main block

    orchestrator = Orchestrator()

    # Example 1: Simple coding task
    print("\n--- Running Simple Coding Workflow ---")
    initial_task_code = {"description": "Write code to calculate factorial of a number.", "type": "coding"}
    final_result_code = orchestrator.execute_workflow(initial_task_code)
    print("\nFinal Result (Coding):")
    print(final_result_code)

    # Example 2: Planning task (simulating multiple steps)
    print("\n--- Running Planning Workflow ---")
    initial_task_plan = {"description": "Plan the architecture for a new microservice.", "type": "planning"}
    final_result_plan = orchestrator.execute_workflow(initial_task_plan)
    print("\nFinal Result (Planning):")
    print(final_result_plan)

    # Example 3: Task with simulated transient failure and retry
    print("\n--- Running Workflow with Simulated Failure and Retry ---")
    initial_task_fail = {"description": "Implement a feature that might fail_task due to transient issues.", "type": "coding"}
    final_result_fail = orchestrator.execute_workflow(initial_task_fail)
    print("\nFinal Result (Simulated Failure):")
    print(final_result_fail)

    # Example 4: Task with simulated review and correction loop
    print("\n--- Running Workflow with Simulated Review and Correction ---")
    initial_task_review = {"description": "Fix bug in authentication module.", "type": "bug_fix"}
    final_result_review = orchestrator.execute_workflow(initial_task_review)
    print("\nFinal Result (Review Loop):")
    print(final_result_review)

    # Example 5: Task simulating tool usage and output integration
    print("\n--- Running Workflow with Simulated Tool Usage ---")
    initial_task_tool_use = {"description": "Implement a simple file writer and lint the code.", "type": "coding_with_tools"}
    final_result_tool_use = orchestrator.execute_workflow(initial_task_tool_use)
    print("\nFinal Result (Tool Usage):")
    print(final_result_tool_use)


if __name__ == "__main__":
    import json # Import json for pretty printing in main block

    orchestrator = Orchestrator()

    # Example 1: Simple coding task
    print("\n--- Running Simple Coding Workflow ---")
    initial_task_code = {"description": "Write code to calculate factorial of a number.", "type": "coding"}
    final_result_code = orchestrator.execute_workflow(initial_task_code)
    print("\nFinal Result (Coding):")
    print(final_result_code)

    # Example 2: Planning task (simulating multiple steps)
    print("\n--- Running Planning Workflow ---")
    initial_task_plan = {"description": "Plan the architecture for a new microservice.", "type": "planning"}
    final_result_plan = orchestrator.execute_workflow(initial_task_plan)
    print("\nFinal Result (Planning):")
    print(final_result_plan)

    # Example 3: Task with simulated transient failure and retry
    print("\n--- Running Workflow with Simulated Failure and Retry ---")
    initial_task_fail = {"description": "Implement a feature that might fail_task due to transient issues.", "type": "coding"}
    final_result_fail = orchestrator.execute_workflow(initial_task_fail)
    print("\nFinal Result (Simulated Failure):")
    print(final_result_fail)

    # Example 4: Task with simulated review and correction loop
    print("\n--- Running Workflow with Simulated Review and Correction ---")
    initial_task_review = {"description": "Fix bug in authentication module.", "type": "bug_fix"}
    final_result_review = orchestrator.execute_workflow(initial_task_review)
    print("\nFinal Result (Review Loop):")
    print(final_result_review)

    # Example 5: Task simulating tool usage and output integration
    print("\n--- Running Workflow with Simulated Tool Usage ---")
    initial_task_tool_use = {"description": "Implement a simple file writer and lint the code.", "type": "coding_with_tools"}
    final_result_tool_use = orchestrator.execute_workflow(initial_task_tool_use)
    print("\nFinal Result (Tool Usage):")
    print(final_result_tool_use)
