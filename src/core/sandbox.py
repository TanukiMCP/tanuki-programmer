import docker
import docker.errors
import os
import threading
import time
from typing import Dict, Any, Optional

# For type hinting the container object
# from docker.models.containers import Container as DockerContainer
# The above import might cause issues with some linters/environments if not directly exposed.
# We'll rely on the runtime type or a more general 'Any' if specific type hinting causes problems.

class CodeExecutionSandbox:
    """
    A secure, isolated code execution environment using Docker containers.
    Supports execution of Python, JavaScript, Java, C++, Go, and Rust.
    """

    def __init__(self, image_name: str = "tanuki-sandbox", dockerfile_path: str = "src/Dockerfile"):
        self.client = docker.from_env()
        self.image_name = image_name
        self.dockerfile_path = dockerfile_path
        self._build_image()

    def _build_image(self):
        """Builds the Docker image for the sandbox."""
        print(f"Building Docker image: {self.image_name} from {self.dockerfile_path}...")
        try:
            # Get the directory of the Dockerfile
            docker_context_path = os.path.dirname(self.dockerfile_path)
            if not docker_context_path:
                docker_context_path = '.' # Assume current directory if path is just a filename

            self.client.images.build(
                path=docker_context_path,
                dockerfile=os.path.basename(self.dockerfile_path),
                tag=self.image_name,
                rm=True  # Remove intermediate containers
            )
            print(f"Docker image {self.image_name} built successfully.")
        except docker.errors.BuildError as e:
            print(f"Error building Docker image: {e}")
            raise

    def execute_code(self,
                     language: str,
                     code: str,
                     inputs: Optional[str] = None,
                     cpu_limit: Optional[str] = "0.5",  # e.g., "0.5" for 50% of one CPU
                     memory_limit: Optional[str] = "128m", # e.g., "128m" for 128MB
                     timeout: int = 10 # seconds
                    ) -> Dict[str, Any]:
        """
        Executes code in an isolated Docker container.

        Args:
            language (str): The programming language (e.g., "python", "javascript", "java", "cpp", "go", "rust").
            code (str): The code to execute.
            inputs (Optional[str]): Standard input to provide to the code.
            cpu_limit (Optional[str]): CPU limit (e.g., "0.5" for 50% of one CPU).
            memory_limit (Optional[str]): Memory limit (e.g., "128m", "1g").
            timeout (int): Maximum execution time in seconds.

        Returns:
            Dict[str, Any]: A dictionary containing stdout, stderr, exit_code, and a timeout flag.
        """
        temp_file_name = ""
        command = []
        file_extension = ""

        if language.lower() == "python":
            file_extension = "py"
            temp_file_name = "script.py"
            command = ["python3", temp_file_name]
        elif language.lower() == "javascript":
            file_extension = "js"
            temp_file_name = "script.js"
            command = ["node", temp_file_name]
        elif language.lower() == "java":
            file_extension = "java"
            temp_file_name = "Main.java" # Java requires class name to match file name
            command = ["sh", "-c", f"javac {temp_file_name} && java Main"]
        elif language.lower() == "cpp":
            file_extension = "cpp"
            temp_file_name = "main.cpp"
            command = ["sh", "-c", f"g++ {temp_file_name} -o a.out && ./a.out"]
        elif language.lower() == "go":
            file_extension = "go"
            temp_file_name = "main.go"
            command = ["sh", "-c", f"go run {temp_file_name}"]
        elif language.lower() == "rust":
            file_extension = "rs"
            temp_file_name = "main.rs"
            command = ["sh", "-c", f"rustc {temp_file_name} && ./main"]
        else:
            return {"stdout": "", "stderr": f"Unsupported language: {language}", "exit_code": 1, "timeout": False}

        # Create a temporary directory for the code file
        temp_dir = f"/tmp/sandbox_code_{os.getpid()}_{threading.get_ident()}"
        os.makedirs(temp_dir, exist_ok=True)
        code_file_path = os.path.join(temp_dir, temp_file_name)

        try:
            with open(code_file_path, "w") as f:
                f.write(code)

            container: Optional[Any] = None # Use Any for now to avoid complex type hinting issues
            result = {"stdout": "", "stderr": "", "exit_code": 1, "timeout": False}
            
            def run_container():
                nonlocal container
                try:
                    container = self.client.containers.run(
                        self.image_name,
                        command=command,
                        detach=True,
                        auto_remove=False, # We'll remove it manually after getting logs
                        network_disabled=True, # Isolate from network
                        mem_limit=memory_limit,
                        cpu_period=100000, # 100ms
                        cpu_quota=int(float(cpu_limit) * 100000) if cpu_limit else -1,
                        volumes={
                            os.path.abspath(temp_dir): {
                                'bind': '/app',
                                'mode': 'ro' # Read-only mount for the code
                            }
                        },
                        working_dir="/app",
                        stdin_open=True # Enable stdin for input
                    )

                    # Provide input if any
                    if inputs and container: # Ensure container is not None before attaching socket
                        sock = container.attach_socket(params={'stdin': 1, 'stream': 1})
                        sock._sock.sendall(inputs.encode('utf-8'))
                        sock.close()

                    if container: # Ensure container is not None before waiting
                        container.wait(timeout=timeout)
                except docker.errors.ContainerError as e:
                    result["stderr"] = e.stderr.decode('utf-8')
                    result["exit_code"] = e.exit_status
                except docker.errors.APIError as e:
                    result["stderr"] = f"Docker API Error: {e}"
                    result["exit_code"] = 1
                except Exception as e:
                    result["stderr"] = f"An unexpected error occurred: {e}"
                    result["exit_code"] = 1
                finally:
                    if container:
                        # Get logs before removing
                        stdout_logs_raw = container.logs(stdout=True, stderr=False)
                        stderr_logs_raw = container.logs(stdout=False, stderr=True)

                        # Decode stdout
                        if stdout_logs_raw is None:
                            result["stdout"] = ""
                        elif isinstance(stdout_logs_raw, bytes):
                            result["stdout"] = stdout_logs_raw.decode('utf-8')
                        else: # Assume it's already a string if not bytes or None
                            result["stdout"] = str(stdout_logs_raw)

                        # Decode stderr
                        decoded_stderr = ""
                        if stderr_logs_raw is None:
                            decoded_stderr = ""
                        elif isinstance(stderr_logs_raw, bytes):
                            decoded_stderr = stderr_logs_raw.decode('utf-8')
                        else: # Assume it's already a string if not bytes or None
                            decoded_stderr = str(stderr_logs_raw)
                        result["stderr"] += decoded_stderr
                        try:
                            # Get exit code if not already set by ContainerError
                            if "exit_code" not in result or result["exit_code"] is None:
                                # Ensure container.id is not None before calling get
                                if container.id:
                                    inspect_result = self.client.containers.get(container.id).wait()
                                    result["exit_code"] = inspect_result["StatusCode"]
                        except Exception as e:
                            print(f"Warning: Could not get final exit code: {e}")
                        container.remove()

            thread = threading.Thread(target=run_container)
            thread.start()
            thread.join(timeout=timeout + 5) # Give a little extra time for Docker cleanup

            if thread.is_alive():
                result["timeout"] = True
                result["stderr"] += "\nExecution timed out."
                if container:
                    try:
                        container.kill()
                        container.remove()
                    except docker.errors.APIError as e:
                        result["stderr"] += f"\nFailed to kill/remove container after timeout: {e}"
            
            # Ensure stdout/stderr are strings
            result["stdout"] = str(result["stdout"]).strip()
            result["stderr"] = str(result["stderr"]).strip()

            return result

        finally:
            # Clean up the temporary code file and directory
            if os.path.exists(code_file_path):
                os.remove(code_file_path)
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)

if __name__ == "__main__":
    sandbox = CodeExecutionSandbox()

    print("\n--- Testing Python ---")
    python_code = """
import sys
print("Hello from Python!")
x = 10
y = 20
print(f"Sum: {x + y}")
input_val = sys.stdin.readline().strip()
print(f"Received input: {input_val}")
"""
    python_inputs = "TestInputPython"
    py_result = sandbox.execute_code("python", python_code, inputs=python_inputs, timeout=5)
    print(f"Python Stdout:\n{py_result['stdout']}")
    print(f"Python Stderr:\n{py_result['stderr']}")
    print(f"Python Exit Code: {py_result['exit_code']}")
    print(f"Python Timeout: {py_result['timeout']}")

    print("\n--- Testing JavaScript ---")
    js_code = """
const readline = require('readline');
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});
console.log("Hello from JavaScript!");
let a = 5;
let b = 7;
console.log(`Product: ${a * b}`);
rl.question('', (input) => {
  console.log(`Received input: ${input}`);
  rl.close();
});
"""
    js_inputs = "TestInputJS"
    js_result = sandbox.execute_code("javascript", js_code, inputs=js_inputs, timeout=5)
    print(f"JavaScript Stdout:\n{js_result['stdout']}")
    print(f"JavaScript Stderr:\n{js_result['stderr']}")
    print(f"JavaScript Exit Code: {js_result['exit_code']}")
    print(f"JavaScript Timeout: {js_result['timeout']}")

    print("\n--- Testing Java ---")
    java_code = """
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        System.out.println("Hello from Java!");
        int num1 = 15;
        int num2 = 3;
        System.out.println("Division: " + (num1 / num2));
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter input: ");
        String input = scanner.nextLine();
        System.out.println("Received input: " + input);
        scanner.close();
    }
}
"""
    java_inputs = "TestInputJava"
    java_result = sandbox.execute_code("java", java_code, inputs=java_inputs, timeout=15) # Java compilation can be slow
    print(f"Java Stdout:\n{java_result['stdout']}")
    print(f"Java Stderr:\n{java_result['stderr']}")
    print(f"Java Exit Code: {java_result['exit_code']}")
    print(f"Java Timeout: {java_result['timeout']}")

    print("\n--- Testing C++ ---")
    cpp_code = """
#include <iostream>
#include <string>

int main() {
    std::cout << "Hello from C++!" << std::endl;
    int x = 100;
    int y = 20;
    std::cout << "Difference: " << (x - y) << std::endl;
    std::string input;
    std::cout << "Enter input: ";
    std::getline(std::cin, input);
    std::cout << "Received input: " << input << std::endl;
    return 0;
}
"""
    cpp_inputs = "TestInputCPP"
    cpp_result = sandbox.execute_code("cpp", cpp_code, inputs=cpp_inputs, timeout=10)
    print(f"C++ Stdout:\n{cpp_result['stdout']}")
    print(f"C++ Stderr:\n{cpp_result['stderr']}")
    print(f"C++ Exit Code: {cpp_result['exit_code']}")
    print(f"C++ Timeout: {cpp_result['timeout']}")

    print("\n--- Testing Go ---")
    go_code = """
package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	fmt.Println("Hello from Go!")
	a := 12
	b := 4
	fmt.Printf("Quotient: %d\\n", a / b)

	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Enter input: ")
	input, _ := reader.ReadString('\\n')
	fmt.Printf("Received input: %s", strings.TrimSpace(input))
}
"""
    go_inputs = "TestInputGo"
    go_result = sandbox.execute_code("go", go_code, inputs=go_inputs, timeout=10)
    print(f"Go Stdout:\n{go_result['stdout']}")
    print(f"Go Stderr:\n{go_result['stderr']}")
    print(f"Go Exit Code: {go_result['exit_code']}")
    print(f"Go Timeout: {go_result['timeout']}")

    print("\n--- Testing Rust ---")
    rust_code = """
use std::io::{self, Write};

fn main() {
    println!("Hello from Rust!");
    let x = 7;
    let y = 3;
    println!("Remainder: {}", x % y);

    print!("Enter input: ");
    io::stdout().flush().unwrap();
    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("Failed to read line");
    println!("Received input: {}", input.trim());
}
"""
    rust_inputs = "TestInputRust"
    rust_result = sandbox.execute_code("rust", rust_code, inputs=rust_inputs, timeout=10)
    print(f"Rust Stdout:\n{rust_result['stdout']}")
    print(f"Rust Stderr:\n{rust_result['stderr']}")
    print(f"Rust Exit Code: {rust_result['exit_code']}")
    print(f"Rust Timeout: {rust_result['timeout']}")

    print("\n--- Testing Timeout ---")
    timeout_code = """
import time
time.sleep(15)
print("This should not print.")
"""
    timeout_result = sandbox.execute_code("python", timeout_code, timeout=5)
    print(f"Timeout Stdout:\n{timeout_result['stdout']}")
    print(f"Timeout Stderr:\n{timeout_result['stderr']}")
    print(f"Timeout Exit Code: {timeout_result['exit_code']}")
    print(f"Timeout Timeout: {timeout_result['timeout']}")

    print("\n--- Testing Error Handling (Python Syntax Error) ---")
    error_code = """
print("Hello"
"""
    error_result = sandbox.execute_code("python", error_code, timeout=5)
    print(f"Error Stdout:\n{error_result['stdout']}")
    print(f"Error Stderr:\n{error_result['stderr']}")
    print(f"Error Exit Code: {error_result['exit_code']}")
    print(f"Error Timeout: {error_result['timeout']}")
