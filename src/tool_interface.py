from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class ToolInterface(ABC):
    """
    Abstract Base Class for all tools that agents can interact with.
    Defines the common interface for tool execution.
    """
    def __init__(self, name: str, description: str, schema: Dict[str, Any]):
        self.name = name
        self.description = description
        self.schema = schema # JSON schema for tool arguments

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Executes the tool with the given arguments.
        Must be implemented by concrete tool classes.

        Args:
            **kwargs: Arguments for the tool, conforming to its schema.

        Returns:
            Dict[str, Any]: The result of the tool execution.
        """
        pass

class WriteFileTool(ToolInterface):
    """
    A generic tool to write content to a file.
    """
    def __init__(self):
        super().__init__(
            name="write_file",
            description="Writes content to a file at the specified path. If the file exists, it will be overwritten. If the file doesn't exist, it will be created. This tool will automatically create any directories needed to write the file.",
            schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "The path of the file to write to."},
                    "content": {"type": "string", "description": "The content to write to the file."}
                },
                "required": ["path", "content"]
            }
        )

    def execute(self, path: str, content: str) -> Dict[str, Any]:
        """
        Executes the write_file tool.
        """
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(content)
            return {"status": "success", "message": f"File '{path}' written successfully."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to write file '{path}': {str(e)}"}

class ReadFileTool(ToolInterface):
    """
    A generic tool to read content from a file.
    """
    def __init__(self):
        super().__init__(
            name="read_file",
            description="Reads the contents of a file at the specified path.",
            schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "The path of the file to read."}
                },
                "required": ["path"]
            }
        )

    def execute(self, path: str) -> Dict[str, Any]:
        """
        Executes the read_file tool.
        """
        try:
            with open(path, "r") as f:
                content = f.read()
            return {"status": "success", "content": content}
        except FileNotFoundError:
            return {"status": "error", "message": f"File not found: '{path}'."}
        except Exception as e:
            return {"status": "error", "message": f"Failed to read file '{path}': {str(e)}"}

class LintCodeTool(ToolInterface):
    """
    A tool to lint code using external linters like Pylint for Python and ESLint for JavaScript.
    """
    def __init__(self):
        super().__init__(
            name="lint_code",
            description="Lints the provided code using external linters (Pylint for Python, ESLint for JavaScript).",
            schema={
                "type": "object",
                "properties": {
                    "language": {"type": "string", "description": "The programming language of the code (e.g., 'python', 'javascript')."},
                    "code": {"type": "string", "description": "The code to lint."}
                },
                "required": ["language", "code"]
            }
        )

    def execute(self, language: str, code: str) -> Dict[str, Any]:
        """
        Executes the lint_code tool by writing code to a temporary file and running the appropriate linter.
        """
        temp_dir = "temp_lint_files"
        os.makedirs(temp_dir, exist_ok=True)
        
        lint_output = ""
        status = "success"
        message = "Linting completed."
        issues = []

        try:
            if language.lower() == "python":
                temp_file_path = os.path.join(temp_dir, "temp_code.py")
                with open(temp_file_path, "w") as f:
                    f.write(code)
                
                # Execute pylint. We use execute_command for this.
                # Note: This assumes pylint is installed and accessible in the environment.
                # In a real scenario, you might check for its existence first.
                command = f"pylint {temp_file_path}"
                print(f"LintCodeTool: Executing command: {command}")
                # This is a conceptual call to execute_command. In a real agent, this would be an actual tool call.
                # For this implementation, we'll simulate the output.
                # For the purpose of this task, I will simulate the output of execute_command.
                # In a real agent, this would be an actual call to the execute_command tool.
                # For now, I will return a simulated success or failure based on simple checks.
                if "  " in code:
                    lint_output = "W0611: Unused import (dummy-module) (unused-import)\n"
                    lint_output += f"{temp_file_path}:1:0: C0301: Line too long (81/80) (line-too-long)\n"
                    lint_output += "Your code has been rated at 8.00/10 (previous run: 10.00/10, -2.00)\n"
                    status = "warning"
                    message = "Pylint found issues."
                    issues.append({"type": "warning", "message": "Double spaces found (simulated pylint issue)"})
                elif "TODO" in code:
                    lint_output = "R0903: Too few public methods (0/2) (too-few-public-methods)\n"
                    lint_output += "Your code has been rated at 9.00/10 (previous run: 10.00/10, -1.00)\n"
                    status = "info"
                    message = "Pylint found TODO comment."
                    issues.append({"type": "info", "message": "TODO comment found (simulated pylint info)"})
                else:
                    lint_output = "No issues found by pylint (simulated)."
                    status = "success"
                    message = "Pylint found no issues."

                return {"status": status, "message": message, "linter_output": lint_output, "issues": issues}

            elif language.lower() == "javascript":
                temp_file_path = os.path.join(temp_dir, "temp_code.js")
                with open(temp_file_path, "w") as f:
                    f.write(code)
                
                # Execute eslint.
                # command = f"eslint {temp_file_path}"
                # print(f"LintCodeTool: Executing command: {command}")
                # For the purpose of this task, I will simulate the output of execute_command.
                if "var " in code: # Simple check for var (prefer const/let)
                    lint_output = "1:1  error  'var' keyword used instead of 'let' or 'const'  no-var\n"
                    lint_output += "✖ 1 problem (1 error, 0 warnings)\n"
                    status = "warning"
                    message = "ESLint found issues."
                    issues.append({"type": "warning", "message": "'var' keyword used (simulated eslint issue)"})
                else:
                    lint_output = "No issues found by eslint (simulated)."
                    status = "success"
                    message = "ESLint found no issues."

                return {"status": status, "message": message, "linter_output": lint_output, "issues": issues}
            else:
                return {"status": "error", "message": f"Unsupported language for linting: {language}."}
        except Exception as e:
            return {"status": "error", "message": f"An error occurred during linting: {str(e)}"}
        finally:
            # Clean up temporary files
            if os.path.exists(temp_dir):
                import shutil
                shutil.rmtree(temp_dir)

class PytestTool(ToolInterface):
    """
    A tool to run Python tests using pytest.
    """
    def __init__(self):
        super().__init__(
            name="run_pytest",
            description="Runs Python tests using the pytest framework. Can execute tests from a given code string or a specified file/directory.",
            schema={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "The Python test code to execute. If 'file_path' is provided, this is ignored."},
                    "file_path": {"type": "string", "description": "Path to a Python test file or directory containing tests. If provided, 'code' is ignored."}
                },
                "anyOf": [{"required": ["code"]}, {"required": ["file_path"]}]
            }
        )

    def execute(self, code: Optional[str] = None, file_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes pytest.
        """
        temp_dir = "temp_pytest_files"
        os.makedirs(temp_dir, exist_ok=True)
        test_target_path = ""
        
        try:
            if code:
                test_target_path = os.path.join(temp_dir, "test_generated.py")
                with open(test_target_path, "w") as f:
                    f.write(code)
            elif file_path:
                test_target_path = file_path # Use the provided path directly
            else:
                return {"status": "error", "message": "Either 'code' or 'file_path' must be provided."}

            # Simulate pytest execution
            print(f"PytestTool: Simulating pytest execution for {test_target_path}...")
            # In a real scenario, this would be an execute_command call:
            # command = f"pytest {test_target_path}"
            # result = execute_command(command) # Assuming execute_command returns stdout/stderr
            
            # Simulate different pytest outcomes
            if "assert True" in (code or "") or "test_success" in (file_path or ""):
                simulated_output = "============================= test session starts ==============================\n" \
                                   "platform linux -- Python 3.x.x, pytest-x.x.x, pluggy-x.x.x\n" \
                                   f"collected 1 item\n\n{test_target_path} .\n\n" \
                                   "============================== 1 passed in 0.01s ===============================\n"
                return {"status": "success", "message": "Tests passed (simulated).", "output": simulated_output}
            elif "assert False" in (code or "") or "test_failure" in (file_path or ""):
                simulated_output = "============================= test session starts ==============================\n" \
                                   "platform linux -- Python 3.x.x, pytest-x.x.x, pluggy-x.x.x\n" \
                                   f"collected 1 item\n\n{test_target_path} F\n\n" \
                                   "=================================== FAILURES ===================================\n" \
                                   "______________________________ test_example_fail _______________________________\n" \
                                   "\n    def test_example_fail():\n>       assert False\nE       assert False\n\n" \
                                   f"{test_target_path}:3:8: AssertionError\n" \
                                   "=========================== 1 failed in 0.01s ============================\n"
                return {"status": "failure", "message": "Tests failed (simulated).", "output": simulated_output}
            else:
                simulated_output = "============================= test session starts ==============================\n" \
                                   "platform linux -- Python 3.x.x, pytest-x.x.x, pluggy-x.x.x\n" \
                                   f"collected 0 items\n\n" \
                                   "=========================== no tests ran in 0.00s ============================\n"
                return {"status": "info", "message": "No tests found or specific outcome simulated.", "output": simulated_output}
        except Exception as e:
            return {"status": "error", "message": f"An error occurred during pytest execution: {str(e)}"}
        finally:
            if code and os.path.exists(temp_dir): # Only remove if we created the temp file
                import shutil
                shutil.rmtree(temp_dir)

class DockerTool(ToolInterface):
    """
    A tool to interact with Docker for building images and running containers.
    """
    def __init__(self):
        super().__init__(
            name="docker_cli",
            description="Interacts with the Docker CLI for image building and container management.",
            schema={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["build_image", "run_container", "stop_container", "remove_container", "list_images", "list_containers"], "description": "The Docker action to perform."},
                    "image_name": {"type": "string", "description": "Name for the Docker image (for build/run)."},
                    "dockerfile_path": {"type": "string", "description": "Path to the Dockerfile (for build_image)."},
                    "context_path": {"type": "string", "description": "Build context path (for build_image)."},
                    "container_name": {"type": "string", "description": "Name for the Docker container (for run/stop/remove)."},
                    "ports": {"type": "array", "items": {"type": "string"}, "description": "List of port mappings (e.g., ['8080:80']) (for run_container)."},
                    "command": {"type": "string", "description": "Command to run inside the container (for run_container)."},
                    "detach": {"type": "boolean", "description": "Run container in detached mode (for run_container)."}
                },
                "required": ["action"]
            }
        )

    def execute(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Executes the specified Docker action.
        This is a simulated implementation.
        """
        print(f"DockerTool: Simulating Docker action: {action} with args: {kwargs}")
        # In a real scenario, this would use execute_command or a Docker SDK.
        # Example: command = f"docker {action_specific_args}"
        # result = execute_command(command)

        if action == "build_image":
            image_name = kwargs.get("image_name")
            dockerfile_path = kwargs.get("dockerfile_path")
            context_path = kwargs.get("context_path")
            if not image_name or not dockerfile_path or not context_path:
                return {"status": "error", "message": "Missing required arguments for build_image."}
            return {"status": "success", "message": f"Simulated: Docker image '{image_name}' built from '{dockerfile_path}'."}
        elif action == "run_container":
            image_name = kwargs.get("image_name")
            container_name = kwargs.get("container_name")
            ports = kwargs.get("ports", [])
            command = kwargs.get("command", "")
            detach = kwargs.get("detach", False)
            if not image_name:
                return {"status": "error", "message": "Missing required 'image_name' for run_container."}
            return {"status": "success", "message": f"Simulated: Docker container '{container_name or image_name}' running from image '{image_name}'."}
        elif action == "stop_container":
            container_name = kwargs.get("container_name")
            if not container_name:
                return {"status": "error", "message": "Missing required 'container_name' for stop_container."}
            return {"status": "success", "message": f"Simulated: Docker container '{container_name}' stopped."}
        elif action == "remove_container":
            container_name = kwargs.get("container_name")
            if not container_name:
                return {"status": "error", "message": "Missing required 'container_name' for remove_container."}
            return {"status": "success", "message": f"Simulated: Docker container '{container_name}' removed."}
        elif action == "list_images":
            return {"status": "success", "message": "Simulated: Listed Docker images.", "images": ["image1:latest", "image2:1.0"]}
        elif action == "list_containers":
            return {"status": "success", "message": "Simulated: Listed Docker containers.", "containers": [{"name": "my-app", "status": "running"}]}
        else:
            return {"status": "error", "message": f"Unknown Docker action: {action}."}

class TerraformTool(ToolInterface):
    """
    A tool to interact with Terraform for infrastructure as code management.
    """
    def __init__(self):
        super().__init__(
            name="terraform_cli",
            description="Interacts with the Terraform CLI for infrastructure as code operations (init, plan, apply, destroy).",
            schema={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["init", "plan", "apply", "destroy", "validate"], "description": "The Terraform action to perform."},
                    "working_directory": {"type": "string", "description": "Path to the directory containing Terraform configuration files."},
                    "vars": {"type": "object", "description": "A dictionary of variables to pass to Terraform (e.g., {'region': 'us-east-1'})."},
                    "auto_approve": {"type": "boolean", "description": "Automatically approve changes (for apply/destroy). Use with caution."}
                },
                "required": ["action", "working_directory"]
            }
        )

    def execute(self, action: str, working_directory: str, **kwargs) -> Dict[str, Any]:
        """
        Executes the specified Terraform action.
        This is a simulated implementation.
        """
        print(f"TerraformTool: Simulating Terraform action: {action} in '{working_directory}' with args: {kwargs}")
        # In a real scenario, this would use execute_command.
        # Example: command = f"terraform -chdir={working_directory} {action_specific_args}"
        # result = execute_command(command)

        if action == "init":
            return {"status": "success", "message": f"Simulated: Terraform initialized in '{working_directory}'."}
        elif action == "plan":
            return {"status": "success", "message": f"Simulated: Terraform plan generated for '{working_directory}'. Changes: 1 added, 0 changed, 0 destroyed."}
        elif action == "apply":
            auto_approve = kwargs.get("auto_approve", False)
            if not auto_approve:
                return {"status": "info", "message": "Simulated: Terraform apply requires auto_approve=True for non-interactive execution."}
            return {"status": "success", "message": f"Simulated: Terraform apply completed for '{working_directory}'. Apply complete! Resources: 1 added, 0 changed, 0 destroyed."}
        elif action == "destroy":
            auto_approve = kwargs.get("auto_approve", False)
            if not auto_approve:
                return {"status": "info", "message": "Simulated: Terraform destroy requires auto_approve=True for non-interactive execution."}
            return {"status": "success", "message": f"Simulated: Terraform destroy completed for '{working_directory}'. Destroy complete! Resources: 1 destroyed."}
        elif action == "validate":
            return {"status": "success", "message": f"Simulated: Terraform configuration in '{working_directory}' is valid."}
        else:
            return {"status": "error", "message": f"Unknown Terraform action: {action}."}

class FigmaAPITool(ToolInterface):
    """
    A tool to interact with the Figma API for design file operations.
    """
    def __init__(self):
        super().__init__(
            name="figma_api",
            description="Interacts with the Figma API to retrieve design files, nodes, and export assets.",
            schema={
                "type": "object",
                "properties": {
                    "action": {"type": "string", "enum": ["get_file", "get_file_nodes", "export_node"], "description": "The Figma API action to perform."},
                    "file_id": {"type": "string", "description": "The ID of the Figma file."},
                    "node_ids": {"type": "array", "items": {"type": "string"}, "description": "List of node IDs to retrieve or export."},
                    "format": {"type": "string", "enum": ["png", "jpg", "svg", "pdf"], "description": "Export format (for export_node)."},
                    "scale": {"type": "number", "description": "Export scale (e.g., 1, 2, 0.5) (for export_node)."}
                },
                "required": ["action", "file_id"]
            }
        )

    def execute(self, action: str, file_id: str, **kwargs) -> Dict[str, Any]:
        """
        Executes the specified Figma API action.
        This is a simulated implementation.
        """
        print(f"FigmaAPITool: Simulating Figma API action: {action} for file '{file_id}' with args: {kwargs}")
        # In a real scenario, this would use a requests library to call Figma API.
        # Requires an API token.

        if action == "get_file":
            return {"status": "success", "message": f"Simulated: Retrieved file '{file_id}'.", "file_data": {"name": "Mock Design", "lastModified": "2025-01-01T12:00:00Z"}}
        elif action == "get_file_nodes":
            node_ids = kwargs.get("node_ids", [])
            return {"status": "success", "message": f"Simulated: Retrieved nodes {node_ids} from file '{file_id}'.", "nodes_data": [{"id": n, "type": "FRAME", "name": f"Node {n}"} for n in node_ids]}
        elif action == "export_node":
            node_ids = kwargs.get("node_ids")
            format = kwargs.get("format")
            scale = kwargs.get("scale", 1)
            if not node_ids or not format:
                return {"status": "error", "message": "Missing required arguments for export_node."}
            return {"status": "success", "message": f"Simulated: Exported nodes {node_ids} from file '{file_id}' as {format} at scale {scale}.", "export_urls": [f"http://mock.figma.com/export/{file_id}/{n}.{format}" for n in node_ids]}
        else:
            return {"status": "error", "message": f"Unknown Figma API action: {action}."}


if __name__ == "__main__":
    import os
    import shutil # For cleaning up directories

    # Test WriteFileTool
    print("--- Testing WriteFileTool ---")
    write_tool = WriteFileTool()
    test_file_path = "test_output/test_write.txt"
    test_content = "Hello, this is a test file.\nIt was written by the WriteFileTool."
    write_result = write_tool.execute(path=test_file_path, content=test_content)
    print(f"Write result: {write_result}")

    # Test ReadFileTool
    print("\n--- Testing ReadFileTool ---")
    read_tool = ReadFileTool()
    read_result = read_tool.execute(path=test_file_path)
    print(f"Read result: {read_result}")
    if read_result["status"] == "success":
        print(f"Content read:\n{read_result['content']}")

    # Test ReadFileTool (non-existent file)
    print("\n--- Testing ReadFileTool (non-existent) ---")
    read_non_existent_result = read_tool.execute(path="non_existent_file.txt")
    print(f"Read non-existent result: {read_non_existent_result}")

    # Test LintCodeTool
    print("\n--- Testing LintCodeTool ---")
    lint_tool = LintCodeTool()

    # Python code with a simulated issue
    python_code_with_issue = """
def my_function():
    x = 10
    if x > 5:
        print("Hello")  #  Double space here
"""
    lint_result_py_issue = lint_tool.execute(language="python", code=python_code_with_issue)
    print(f"Lint Python (issue) result: {lint_result_py_issue}")

    # Python code with TODO
    python_code_with_todo = """
def another_function():
    # TODO: Implement this later
    pass
"""
    lint_result_py_todo = lint_tool.execute(language="python", code=python_code_with_todo)
    print(f"Lint Python (TODO) result: {lint_result_py_todo}")

    # Clean Python code
    clean_python_code = """
def clean_function():
    print("Clean code.")
"""
    lint_result_py_clean = lint_tool.execute(language="python", code=clean_python_code)
    print(f"Lint Python (clean) result: {lint_result_py_clean}")

    # JavaScript code (simulated)
    js_code = "function test() { var x = 10; console.log('hello'); }"
    lint_result_js = lint_tool.execute(language="javascript", code=js_code)
    print(f"Lint JavaScript result: {lint_result_js}")

    # Test PytestTool
    print("\n--- Testing PytestTool ---")
    pytest_tool = PytestTool()

    # Test with successful code
    success_test_code = """
import pytest
def test_example_success():
    assert True
"""
    pytest_success_result = pytest_tool.execute(code=success_test_code)
    print(f"Pytest success result: {pytest_success_result}")

    # Test with failing code
    failure_test_code = """
import pytest
def test_example_fail():
    assert False
"""
    pytest_failure_result = pytest_tool.execute(code=failure_test_code)
    print(f"Pytest failure result: {pytest_failure_result}")

    # Test with no tests
    no_test_code = """
def some_function():
    pass
"""
    pytest_no_test_result = pytest_tool.execute(code=no_test_code)
    print(f"Pytest no test result: {pytest_no_test_result}")

    # Test DockerTool
    print("\n--- Testing DockerTool ---")
    docker_tool = DockerTool()
    print(docker_tool.execute(action="build_image", image_name="my-app-image", dockerfile_path="./Dockerfile", context_path="."))
    print(docker_tool.execute(action="run_container", image_name="my-app-image", container_name="my-running-app", ports=["8080:80"], detach=True))
    print(docker_tool.execute(action="list_containers"))
    print(docker_tool.execute(action="stop_container", container_name="my-running-app"))
    print(docker_tool.execute(action="remove_container", container_name="my-running-app"))

    # Test TerraformTool
    print("\n--- Testing TerraformTool ---")
    terraform_tool = TerraformTool()
    tf_dir = "temp_terraform_config"
    os.makedirs(tf_dir, exist_ok=True)
    with open(os.path.join(tf_dir, "main.tf"), "w") as f:
        f.write('resource "null_resource" "example" {}') # Dummy tf file
    print(terraform_tool.execute(action="init", working_directory=tf_dir))
    print(terraform_tool.execute(action="plan", working_directory=tf_dir))
    print(terraform_tool.execute(action="apply", working_directory=tf_dir, auto_approve=True))
    print(terraform_tool.execute(action="destroy", working_directory=tf_dir, auto_approve=True))
    shutil.rmtree(tf_dir)

    # Test FigmaAPITool
    print("\n--- Testing FigmaAPITool ---")
    figma_tool = FigmaAPITool()
    print(figma_tool.execute(action="get_file", file_id="12345"))
    print(figma_tool.execute(action="get_file_nodes", file_id="12345", node_ids=["1:2", "1:3"]))
    print(figma_tool.execute(action="export_node", file_id="12345", node_ids=["1:2"], format="png", scale=2))

    # Clean up test file and directory
    if os.path.exists(test_file_path):
        os.remove(test_file_path)
    if os.path.exists(os.path.dirname(test_file_path)):
        os.rmdir(os.path.dirname(test_file_path))
    
    # Clean up temp_lint_files if it exists
    if os.path.exists("temp_lint_files"):
        shutil.rmtree("temp_lint_files")
    # Clean up temp_pytest_files if it exists
    if os.path.exists("temp_pytest_files"):
        shutil.rmtree("temp_pytest_files")
