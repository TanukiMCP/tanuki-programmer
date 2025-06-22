# Local Deployment with Ollama for Tanuki-Programmer

This guide provides step-by-step instructions for setting up Tanuki-Programmer to run locally using Ollama, leveraging the fine-tuned Mistral-3B backbone model and specialized LoRA adapters.

## Prerequisites

Before you begin, ensure you have the following:

1.  **Ollama Installed:** Download and install Ollama from [ollama.ai](https://ollama.ai/).
2.  **Git Installed:** For cloning the Tanuki-Programmer repository.
3.  **Python 3.9+ Installed:** With `pip` for dependency management.
4.  **Sufficient Hardware:** Ensure your system meets the memory and VRAM requirements for running Mistral-3B (quantized) and multiple LoRA adapters.

## 1. Clone the Tanuki-Programmer Repository

First, clone the Tanuki-Programmer repository to your local machine:

```bash
git clone https://github.com/your-repo/tanuki-programmer.git
cd tanuki-programmer
```
*(Note: Replace `https://github.com/your-repo/tanuki-programmer.git` with the actual repository URL once available.)*

## 2. Set Up Python Environment and Dependencies

It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r src/requirements.txt
```

## 3. Download and Load the Mistral-3B GGUF Model with Ollama

The Tanuki-Programmer is fine-tuned on a Mistral-3B backbone. You will need to download a compatible GGUF version of Mistral-3B and load it into Ollama.

1.  **Download Mistral-3B GGUF:**
    You can pull a standard Mistral model directly via Ollama:
    ```bash
    ollama pull mistral
    ```
    Alternatively, if a specific fine-tuned GGUF version of Mistral-3B is provided for Tanuki-Programmer, you would download that file (e.g., `tanuki-mistral-3b-q4_k_m.gguf`) and import it:
    ```bash
    ollama create tanuki-mistral-3b -f ./path/to/Modelfile
    # Example Modelfile content:
    # FROM ./tanuki-mistral-3b-q4_k_m.gguf
    # PARAMETER stop "### Response"
    # PARAMETER stop "### Instruction"
    # PARAMETER stop "### Example"
    ```
    *(Note: The exact model name and Modelfile parameters might vary based on the final fine-tuning and quantization. Refer to the model release notes for precise details.)*

2.  **Verify Ollama Model:**
    Ensure Ollama lists the model:
    ```bash
    ollama list
    ```
    You should see `mistral` or `tanuki-mistral-3b` in the list.

## 4. Place LoRA Adapters

The specialized agents in Tanuki-Programmer utilize LoRA adapters. These adapters need to be accessible by the `Adapter Loader/Unloader` module.

Create a dedicated directory for your LoRA adapters, for example, `models/lora_adapters/`.

```bash
mkdir -p models/lora_adapters
```

Place all your `.safetensors` LoRA adapter files into this directory. The `Adapter Loader/Unloader` will dynamically load them as needed.

## 5. Configure Tanuki-Programmer to Use Ollama

Tanuki-Programmer will need to know which Ollama model to use and where to find the LoRA adapters. This will typically be configured via a configuration file.

Create a configuration file, for example, `config/tanuki_config.json`:

```json
{
  "ollama_base_url": "http://localhost:11434",
  "ollama_model_name": "tanuki-mistral-3b",
  "lora_adapter_path": "models/lora_adapters/",
  "agent_config": {
    "tanuki-coder": {
      "adapter_file": "tanuki-coder-lora.safetensors"
    },
    "tanuki-debugger": {
      "adapter_file": "tanuki-debugger-lora.safetensors"
    }
    // ... other agents and their adapter files
  }
}
```
*(Note: The exact structure of `config/tanuki_config.json` is conceptual and will depend on the final implementation of the `Orchestrator` and `Adapter Loader/Unloader` modules. Ensure the `ollama_model_name` matches the name you used when pulling/creating the model in Ollama.)*

## 6. Run Tanuki-Programmer

Once configured, you can run the Tanuki-Programmer. The exact command will depend on the implemented CLI or entry point.

Example (conceptual):

```bash
python src/main.py --config config/tanuki_config.json
```

Follow the instructions for the Tanuki-Programmer CLI or web UI to interact with the system.

This setup allows you to run Tanuki-Programmer locally, leveraging Ollama for the Mistral-3B backbone and dynamically loading LoRA adapters for specialized agent capabilities.
