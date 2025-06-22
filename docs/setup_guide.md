# Tanuki-Programmer Comprehensive Setup Guide

This guide provides comprehensive instructions for setting up the Tanuki-Programmer development environment, including prerequisites, local execution, Docker setup, and basic usage of the CLI and API.

## 1. Prerequisites

Ensure you have the following software installed on your system:

-   **Git:** For cloning the repository.
-   **Python 3.9+:** With `pip` for dependency management.
-   **Docker:** For building and running containerized environments (essential for the code execution sandbox and full system containerization).
-   **Ollama:** (Optional, for local LLM inference) Download and install from [ollama.ai](https://ollama.ai/).
-   **Google Cloud SDK (gcloud CLI):** (Optional, for GCP deployments) Install from [cloud.google.com/sdk](https://cloud.google.com/sdk).

## 2. Initial Setup

### 2.1. Clone the Repository

```bash
git clone https://github.com/your-repo/tanuki-programmer.git
cd tanuki-programmer
```
*(Note: Replace `https://github.com/your-repo/tanuki-programmer.git` with the actual repository URL once available.)*

### 2.2. Set Up Python Virtual Environment

It is highly recommended to use a Python virtual environment to manage dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2.3. Install Python Dependencies

Install all required Python packages:

```bash
pip install -r src/requirements.txt
```

## 3. Docker Setup

The Tanuki-Programmer leverages Docker for its secure code execution sandbox and for containerizing the entire system for deployment.

### 3.1. Build the Code Execution Sandbox Image

The `src/Dockerfile` is used to build the multi-language code execution sandbox. This image is crucial for the `CodeExecutionSandbox` component.

```bash
docker build -t tanuki-sandbox -f src/Dockerfile .
```
*(Note: This command builds the sandbox image. The main application Dockerfile is separate.)*

### 3.2. Build the Main Application Docker Image

The main `Dockerfile` (located at the root of the project, copied to `src/Dockerfile` for this task) containerizes the entire Tanuki-Programmer system, including the API and core logic.

```bash
docker build -t tanuki-programmer-app -f src/Dockerfile .
```

## 4. Local LLM Setup (with Ollama)

If you plan to run the LLM inference locally using Ollama:

1.  **Download Mistral-3B GGUF Model:**
    Pull a standard Mistral model via Ollama:
    ```bash
    ollama pull mistral
    ```
    Or, if a specific fine-tuned GGUF version of Mistral-3B is provided for Tanuki-Programmer (e.g., `tanuki-mistral-3b-q4_k_m.gguf`), import it:
    ```bash
    ollama create tanuki-mistral-3b -f ./path/to/Modelfile
    # Example Modelfile content:
    # FROM ./tanuki-mistral-3b-q4_k_m.gguf
    # PARAMETER stop "### Response"
    # PARAMETER stop "### Instruction"
    # PARAMETER stop "### Example"
    ```
    Verify the model is loaded: `ollama list`

2.  **Place LoRA Adapters:**
    Create a directory for your LoRA adapters (e.g., `models/lora_adapters/`) and place all `.safetensors` files there.
    ```bash
    mkdir -p models/lora_adapters
    # Copy your .safetensors files here
    ```

3.  **Configure Tanuki-Programmer:**
    Create or update `config/tanuki_config.json` to point to your Ollama setup and LoRA adapters.
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

## 5. Running Tanuki-Programmer Locally

### 5.1. Using the Command-Line Interface (CLI)

The CLI (`src/cli.py`) provides direct interaction for programming tasks.

```bash
python src/cli.py run "Write a Python function to reverse a string."
python src/cli.py config set ollama_model_name my-custom-mistral
python src/cli.py models list
```

### 5.2. Using the Web-based UI

The simple web UI (`web_ui/`) allows for interactive demonstration.

1.  **Start the Web Server:**
    ```bash
    python src/web_server.py
    ```
    This will start a server, typically on `http://localhost:8000/`.

2.  **Access the UI:**
    Open your web browser and navigate to `http://localhost:8000/`.

### 5.3. Using the API Endpoint

The FastAPI endpoint (`src/api.py`) allows programmatic access.

1.  **Start the API Server:**
    ```bash
    uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
    ```
    The `--reload` flag is useful for development. For production, remove it.

2.  **Access API Documentation:**
    Once the server is running, open your browser to `http://localhost:8000/docs` for the OpenAPI (Swagger UI) documentation.

3.  **Make API Requests:**
    Use `curl` or any API client to interact with the endpoints. Remember to include the `X-API-Key` header.

    ```bash
    curl -X GET "http://localhost:8000/health" \
         -H "X-API-Key: supersecretapikey123"

    curl -X POST "http://localhost:8000/run_task" \
         -H "X-API-Key: supersecretapikey123" \
         -H "Content-Type: application/json" \
         -d '{
           "task_description": "Generate a simple HTML page with a 'Hello World' heading.",
           "file_paths": ["index.html"]
         }'
    ```

## 6. Google Cloud Platform (GCP) Deployment (Conceptual)

For deploying the Tanuki-Programmer to GCP, refer to the `deploy/gcp/` directory.

-   **`deploy/gcp/cloudbuild.yaml`:** Defines the CI/CD pipeline for building the Docker image and deploying to Cloud Run.
-   **`deploy/gcp/cloudrun_service.yaml`:** Defines the Cloud Run service configuration.

You will need to have `gcloud CLI` configured and authenticated to your GCP project to use these.

This guide should provide a solid foundation for setting up and interacting with the Tanuki-Programmer.
