# Use a Python base image for the application
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Install system dependencies required for Python packages
# and potentially for the sandbox if it runs within this container
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    # Add any other system dependencies required by your Python packages or tools
    # For example, if you need nodejs, openjdk, etc. for the sandbox, install them here
    # For now, assuming sandbox runs in separate containers or is pre-built
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy requirements file first to leverage Docker cache
COPY src/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# --- Model and Adapter Handling (Conceptual) ---
# In a production setup, you might:
# 1. Pre-download GGUF model and LoRA adapters and COPY them into the image.
#    Example: COPY models/mistral-3b-q4_k_m.gguf /app/models/
#    Example: COPY models/lora_adapters/ /app/models/lora_adapters/
# 2. Or, download them at runtime from a cloud storage bucket (e.g., GCS).
#    This would require configuring authentication and download scripts.
# For this task, we assume they will be available or downloaded by the application logic.
# Ensure your application's config (e.g., config/tanuki_config.json) points to correct paths.

# Create a dedicated user for security
RUN groupadd --system tanuki && \
    useradd --system --gid tanuki --shell /bin/bash --create-home tanuki

# Switch to the tanuki user
USER tanuki

# Expose the port if the application runs a web server (e.g., for the UI or an API)
# Assuming the web server runs on port 8000 as per src/web_server.py
EXPOSE 8000

# Define the entrypoint for the application
# This assumes orchestrator.py is the main entry point.
# If you have a different main script or need to run the web server, adjust accordingly.
# Command to run the FastAPI application with Uvicorn
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
