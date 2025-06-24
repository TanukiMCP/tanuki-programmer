import os
import json
import itertools
from typing import List, Dict, Any, Callable, Optional
from datasets import load_dataset
from tqdm import tqdm
import re

class DataSynthesisPipeline:
    """
    Manages the data synthesis pipeline, including downloading, processing,
    transforming, and storing datasets for LLM training.
    """

    def __init__(self, output_dir: str = "data/synthesized"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"DataSynthesisPipeline initialized. Output directory: {self.output_dir}")

    def _extract_docstring(self, python_code: str) -> str:
        """
        Extracts the docstring from a Python function.
        This is a simplified implementation.
        """
        try:
            # Find the first triple-quoted string
            match = re.search(r'"""(.*?)"""', python_code, re.DOTALL)
            if match:
                return match.group(1).strip()
            match = re.search(r"'''(.*?)'''", python_code, re.DOTALL)
            if match:
                return match.group(1).strip()
        except Exception:
            pass
        return "No docstring found."

    def download_and_process_dataset(self, dataset_name: str, split: str = "train", num_samples: int = -1) -> List[Dict[str, Any]]:
        """
        Downloads and performs initial processing of a dataset from Hugging Face.

        Args:
            dataset_name (str): Name of the dataset on Hugging Face (e.g., "bigcode/the-stack-v2").
            split (str): The dataset split to download (e.g., "train", "test").
            num_samples (int): Number of samples to retrieve. Use -1 for all available.

        Returns:
            List[Dict[str, Any]]: A list of processed data samples.
        """
        print(f"Downloading and processing dataset: {dataset_name}, split: {split}...")
        try:
            dataset = load_dataset(dataset_name, split=split, streaming=True)

            processed_data = []
            # Use itertools.islice for streaming datasets to limit samples
            data_iterator = itertools.islice(dataset, num_samples) if num_samples != -1 else dataset

            for i, item in enumerate(tqdm(data_iterator, desc=f"Processing {dataset_name}")):
                if dataset_name == "bigcode/the-stack-v2":
                    processed_data.append({
                        "id": item.get("hexsha", f"synthetic_id_{i}"),
                        "content": item.get("content", ""),
                        "language": item.get("lang", "unknown"),
                        "path": item.get("path", "")
                    })
                elif dataset_name == "microsoft/CodeXGLUE":
                    # Assuming "code-to-text" sub-dataset for CodeXGLUE
                    processed_data.append({
                        "id": f"codexglue_id_{i}",
                        "code": item.get("code", ""),
                        "text": item.get("text", "")
                    })
                else:
                    processed_data.append({"id": f"generic_id_{i}", "data": item})

            print(f"Finished processing {len(processed_data)} samples from {dataset_name}.")
            return processed_data
        except Exception as e:
            print(f"Error downloading or processing dataset {dataset_name}: {e}")
            return []

    def transform_to_react_example(self,
                                   data_sample: Dict[str, Any],
                                   agent_type: str,
                                   synthesis_strategy: Callable[[Dict[str, Any]], Dict[str, Any]]
                                  ) -> Optional[Dict[str, Any]]:
        """
        Transforms a raw data sample into a ReAct-style training example.

        Args:
            data_sample (Dict[str, Any]): The raw data sample.
            agent_type (str): The type of agent this example is for (e.g., "tanuki-coder").
            synthesis_strategy (Callable): A function implementing the specific synthesis logic
                                           for the given agent type.

        Returns:
            Optional[Dict[str, Any]]: A ReAct-style example, or None if transformation fails.
        """
        try:
            react_example = synthesis_strategy(data_sample)
            react_example["agent_type"] = agent_type
            return react_example
        except Exception as e:
            print(f"Error transforming data sample for {agent_type}: {e}")
            return None

    def synthesize_coder_example(self, data_sample: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesis strategy for 'tanuki-coder' agent.
        Generates a prompt for code generation and a simulated ReAct trace.
        """
        code_content = data_sample.get("content", data_sample.get("code", "print('Hello World')"))
        language = data_sample.get("language", "python")
        
        # Simulate a simple code generation task
        prompt = f"Write a {language} function that takes no arguments and prints 'Hello World'."
        thought = "I need to write a simple function in the specified language. I will use the print statement."
        action = f"Tool: write_file\nArgs: {{'path': 'src/temp_code.{language}', 'content': '{code_content}'}}"
        observation = "File written successfully."
        thought_final = "The code has been generated and written to a file. Task complete."
        action_final = "Finish: Simulated code generation complete."

        return {
            "prompt": prompt,
            "completion": f"Thought: {thought}\nAction: {action}\nObservation: {observation}\nThought: {thought_final}\nAction: {action_final}"
        }

    def synthesize_debugger_example(self, data_sample: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesis strategy for 'tanuki-debugger' agent.
        Generates a prompt for debugging and a simulated ReAct trace.
        """
        code_content = data_sample.get("content", data_sample.get("code", "def bug(): return 1/0"))
        language = data_sample.get("language", "python")
        
        # Simulate a simple debugging task
        prompt = f"Debug the following {language} code:\n```\n{code_content}\n```\nIt is causing an error."
        thought = "I need to identify the error in the provided code. I will simulate running it in the sandbox."
        action = f"Tool: execute_code\nArgs: {{'language': '{language}', 'code': '{code_content}'}}"
        observation = "Stderr: DivisionByZeroError. Line 1: return 1/0"
        thought_final = "The error is a division by zero. I need to fix it."
        action_final = "Finish: Simulated debugging complete."

        return {
            "prompt": prompt,
            "completion": f"Thought: {thought}\nAction: {action}\nObservation: {observation}\nThought: {thought_final}\nAction: {action_final}"
        }

    def synthesize_reviewer_example(self, data_sample: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesis strategy for 'tanuki-reviewer' agent.
        Generates a prompt for code review and a simulated ReAct trace.
        """
        code_content = data_sample.get("content", data_sample.get("code", "x=1;y=2;"))
        language = data_sample.get("language", "python")
        
        # Simulate a simple code review task
        prompt = f"Review the following {language} code for style and best practices:\n```\n{code_content}\n```"
        thought = "I need to check the code for common style issues and suggest improvements. I will use a linting tool."
        action = f"Tool: lint_code\nArgs: {{'language': '{language}', 'code': '{code_content}'}}"
        observation = "Status: warning, Message: Potential style issue: double spaces found."
        thought_final = "The linter found a style issue. I will suggest fixing it."
        action_final = "Finish: Simulated code review complete."

        return {
            "prompt": prompt,
            "completion": f"Thought: {thought}\nAction: {action}\nObservation: {observation}\nThought: {thought_final}\nAction: {action_final}"
        }

    def synthesize_python_dev_example(self, data_sample: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Synthesis strategy for python development examples.
        """
        python_code = data_sample.get("content") or data_sample.get("text")
        if not python_code:
            return None

        docstring = self._extract_docstring(python_code)
        instruction = f"Implement the following Python function: {docstring}"
        
        return {
            "instruction": instruction,
            "thought": "I need to analyze the Python requirements, write clean code, and validate it using Python tools.",
            "tool_calls": [
                {"tool": "write_file", "content": python_code, "path": "src/solution.py"},
                {"tool": "run_terminal_cmd", "command": "python -m py_compile src/solution.py"},
            ],
            "final_answer": python_code
        }

    def get_synthesis_strategy(self, agent_type: str) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
        """Returns the appropriate synthesis strategy function for a given agent type."""
        strategies = {
            "tanuki-coder": self.synthesize_coder_example,
            "tanuki-debugger": self.synthesize_debugger_example,
            "tanuki-reviewer": self.synthesize_reviewer_example,
            "tanuki-python-dev": self.synthesize_python_dev_example,
        }
        strategy = strategies.get(agent_type)
        if not strategy:
            raise ValueError(f"No synthesis strategy found for agent type: {agent_type}")
        return strategy

    def generate_and_store_react_data(self,
                                      dataset_name: str,
                                      agent_type: str,
                                      split: str = "train",
                                      num_samples: int = 1000):
        """
        Generates ReAct-style training data for a specific agent type and stores it.

        Args:
            dataset_name (str): The source dataset name (e.g., "bigcode/the-stack-v2").
            agent_type (str): The target agent type (e.g., "tanuki-coder").
            split (str): The dataset split to use.
            num_samples (int): Number of samples to process from the raw dataset.
        """
        print(f"Generating ReAct data for agent '{agent_type}' from '{dataset_name}'...")
        raw_data = self.download_and_process_dataset(dataset_name, split, num_samples)
        
        if not raw_data:
            print(f"No raw data to process for {dataset_name}.")
            return

        synthesis_strategy = self.get_synthesis_strategy(agent_type)
        
        react_examples = []
        for sample in tqdm(raw_data, desc=f"Transforming to ReAct for {agent_type}"):
            react_example = self.transform_to_react_example(sample, agent_type, synthesis_strategy)
            if react_example:
                react_examples.append(react_example)

        output_file = os.path.join(self.output_dir, f"{agent_type}_{split}_react_data.jsonl")
        self._store_data(react_examples, output_file)
        print(f"Successfully generated and stored {len(react_examples)} ReAct examples for '{agent_type}' in '{output_file}'.")

    def _store_data(self, data: List[Dict[str, Any]], file_path: str):
        """
        Stores the synthesized data in a JSONL format.
        Implements basic data versioning by overwriting or appending.
        For robust versioning, DVC or similar tools would be used.
        """
        print(f"Storing data to {file_path}...")
        with open(file_path, "w") as f:
            for entry in data:
                f.write(json.dumps(entry) + "\n")
        print("Data storage complete.")

def extract_docstring(python_code: str) -> str:
    """
    Extracts the docstring from a Python function.
    This is a simplified implementation.
    """
    try:
        # Find the first triple-quoted string
        match = re.search(r'\"\"\"(.*?)\"\"\"', python_code, re.DOTALL)
        if match:
            return match.group(1).strip()
        match = re.search(r"'''(.*?)'''", python_code, re.DOTALL)
        if match:
            return match.group(1).strip()
    except Exception:
        pass
    return "No docstring found."


def synthesize_python_development_data(example):
    """
    Synthesizes a single training example from a Python code snippet.
    """
    python_code = example.get("content") or example.get("text")
    if not python_code:
        return None

    docstring = extract_docstring(python_code)
    instruction = f"Implement the following Python function: {docstring}"
    
    return {
        "instruction": instruction,
        "thought": "I need to analyze the Python requirements, write clean code, and validate it using Python tools.",
        "tool_calls": [
            {"tool": "write_file", "content": python_code, "path": "src/solution.py"},
            {"tool": "run_terminal_cmd", "command": "python -m py_compile src/solution.py"},
        ],
        "final_answer": python_code
    }

def process_dataset(dataset_name: str, split: str, output_dir: str):
    """
    Downloads a dataset from Hugging Face, processes it, and saves it to disk.
    """
    print(f"Loading dataset {dataset_name}...")
    dataset = load_dataset(dataset_name, split=split, streaming=True) # Use streaming for large datasets

    processed_dataset = map(synthesize_python_development_data, dataset)
    
    # In a real pipeline, you would save this processed dataset to a file or database.
    # For this example, we'll just print a few examples.
    print("Processing dataset...")
    for i, example in enumerate(processed_dataset):
        if example:
            print(f"--- Example {i+1} ---")
            print(example)
        if i >= 4: # Print first 5 valid examples
            break

if __name__ == "__main__":
    pipeline = DataSynthesisPipeline()

    # Generate data for tanuki-coder
    print("\n--- Generating Data for tanuki-coder ---")
    pipeline.generate_and_store_react_data(
        dataset_name="bigcode/the-stack-v2",
        agent_type="tanuki-coder",
        num_samples=50 # Small number for quick test
    )

    # Generate data for tanuki-debugger
    print("\n--- Generating Data for tanuki-debugger ---")
    pipeline.generate_and_store_react_data(
        dataset_name="microsoft/CodeXGLUE", # Using CodeXGLUE for debugger examples
        agent_type="tanuki-debugger",
        num_samples=50 # Small number for quick test
    )

    # Generate data for tanuki-reviewer
    print("\n--- Generating Data for tanuki-reviewer ---")
    pipeline.generate_and_store_react_data(
        dataset_name="bigcode/the-stack-v2",
        agent_type="tanuki-reviewer",
        num_samples=50 # Small number for quick test
    )

    # Example for generating data for the 'tanuki-python-dev' agent
    pipeline.generate_and_store_react_data(
        dataset_name="bigcode/the-stack-v2",
        agent_type="tanuki-python-dev",
        split="train",
        num_samples=100 # small number for demonstration
    )

    print("\nData synthesis pipeline demonstration complete.")

    # Example usage:
    # This will process the python subset of 'bigcode/the-stack-v2'
    # In a real scenario, you would run this for each dataset needed for the agents.
    process_dataset(
        dataset_name="bigcode/the-stack-v2",
        split="train",
        output_dir="data/processed"
    )
