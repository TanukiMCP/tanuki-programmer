# Tanuki-Programmer Troubleshooting Guide

This guide provides solutions to common issues you might encounter while setting up, running, or developing with Tanuki-Programmer.

## 1. General Issues

### Issue: `command not found` or `python: No such file or directory`

**Problem:** The system cannot find the Python executable or a specific command.

**Solution:**
-   Ensure Python is installed and added to your system's PATH.
-   If using a virtual environment, ensure it is activated (`source venv/bin/activate`).
-   Verify the command is correctly spelled and available in your PATH.

### Issue: `ModuleNotFoundError: No module named '...'`

**Problem:** A required Python package is not found.

**Solution:**
-   Ensure you have installed all dependencies from `src/requirements.txt`:
    ```bash
    pip install -r src/requirements.txt
    ```
-   If using a virtual environment, ensure it is activated.
-   If the module is part of the project, verify the `PYTHONPATH` is correctly set or that you are running scripts from the project root or `src/` directory.

## 2. Docker-Related Issues

### Issue: `docker: command not found` or `Cannot connect to the Docker daemon`

**Problem:** Docker is not installed, not running, or your user does not have permissions to access the Docker daemon.

**Solution:**
-   Ensure Docker Desktop (Windows/macOS) or Docker Engine (Linux) is installed and running.
-   On Linux, add your user to the `docker` group: `sudo usermod -aG docker $USER` and then log out and back in for the changes to take effect.

### Issue: `Error building Docker image: ...`

**Problem:** The Docker image build process failed.

**Solution:**
-   Carefully read the error messages in the build log. They usually indicate missing packages, syntax errors in the Dockerfile, or issues with the build context.
-   Ensure all `RUN` commands have necessary dependencies installed.
-   Verify file paths in `COPY` commands are correct relative to the build context.

### Issue: `Error: No such container: ...` or `Container exited with non-zero code`

**Problem:** A Docker container failed to start or exited unexpectedly.

**Solution:**
-   Check the container logs for detailed error messages: `docker logs <container_id_or_name>`.
-   Ensure the `CMD` or `ENTRYPOINT` in your Dockerfile is correct and the application starts successfully within the container.
-   Verify that all necessary files are copied into the container.

## 3. Ollama-Related Issues

### Issue: `ollama: command not found` or `Error: could not connect to ollama`

**Problem:** Ollama is not installed, not running, or the Tanuki-Programmer cannot connect to it.

**Solution:**
-   Ensure Ollama is installed and running on your system.
-   Verify the Ollama server is accessible at the configured `ollama_base_url` (default: `http://localhost:11434`). Check firewall settings.
-   Ensure the specified `ollama_model_name` is correctly pulled and available in Ollama (`ollama list`).

### Issue: LLM inference is slow or Out-Of-Memory (OOM) errors

**Problem:** The LLM model requires more resources than available, or inference is inefficient.

**Solution:**
-   **Quantization:** Ensure you are using a quantized GGUF model (e.g., `Q4_K_M`) for reduced memory footprint.
-   **Hardware:** Verify your system has sufficient RAM and VRAM. LLMs are memory-intensive.
-   **Ollama Settings:** Adjust Ollama's resource usage if possible.
-   **Batch Size:** If applicable, reduce the batch size for inference.
-   **LoRA Adapters:** Ensure only necessary LoRA adapters are loaded. The `Adapter Loader/Unloader` should manage this dynamically.

## 4. API and UI Issues

### Issue: `Connection refused` when accessing API or UI

**Problem:** The web server (Uvicorn for API, `web_server.py` for UI) is not running or is not accessible on the specified port.

**Solution:**
-   Ensure the respective server script is running (`python src/web_server.py` or `uvicorn src.api:app ...`).
-   Verify the port (default 8000) is not already in use by another application.
-   Check firewall settings if accessing from a different machine.

### Issue: `401 Unauthorized` or `403 Forbidden` from API

**Problem:** Authentication or authorization failed.

**Solution:**
-   Ensure you are providing the `X-API-Key` header with a valid API key.
-   Verify the API key has the necessary roles for the endpoint you are trying to access (e.g., `user` role for `/run_task`).
-   Check `src/api.py` for `VALID_API_KEYS` and `has_role` logic.

### Issue: `429 Too Many Requests` from API

**Problem:** Rate limit exceeded.

**Solution:**
-   You have sent too many requests within the allowed time frame. Wait for a minute and try again.
-   Adjust your client's request rate.
-   (For development) You can temporarily increase `RATE_LIMIT_PER_MINUTE` in `src/api.py` for testing.

## 5. Code Execution Sandbox Issues

### Issue: Code execution fails or produces unexpected output

**Problem:** The code executed in the sandbox has errors, or the sandbox environment is misconfigured.

**Solution:**
-   Check the `stderr` output from the `execute_code` result for compiler/interpreter errors or runtime exceptions.
-   Verify the code itself is correct for the specified language.
-   Ensure the Docker image for the sandbox (`tanuki-sandbox`) is correctly built and contains the necessary language runtimes and compilers.
-   Check resource limits (CPU, memory, timeout) in `execute_code` call; too restrictive limits can cause failures.

If you encounter an issue not covered here, please refer to the project's documentation or open an issue on the project's GitHub repository.
