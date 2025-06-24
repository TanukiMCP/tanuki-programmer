FROM python:3.10-slim

WORKDIR /app

# Copy and install requirements
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the orchestrator
# This will be updated once the orchestrator.py is implemented
CMD ["uvicorn", "orchestrator:app", "--host", "0.0.0.0", "--port", "8080"] 