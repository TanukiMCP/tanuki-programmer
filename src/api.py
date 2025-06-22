from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import time
from typing import Optional, Dict
from collections import defaultdict

# Conceptual imports for Tanuki-Programmer core components
# from orchestrator import Orchestrator
# from resource_management import ResourceManager
# from tool_interface import ToolInterface

app = FastAPI(
    title="Tanuki-Programmer API",
    description="API for interacting with the Tanuki-Programmer LLM for code generation and analysis.",
    version="0.1.0",
)

# --- API Security: Authentication, Authorization, Rate Limiting ---

# 1. Authentication (API Key)
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# In a real application, store API keys securely (e.g., environment variables, secret manager)
# and validate against a database.
VALID_API_KEYS = {
    "supersecretapikey123": {"user": "admin", "roles": ["admin", "user"]},
    "anotherkey456": {"user": "developer", "roles": ["user"]},
}

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return api_key

# 2. Authorization (Role-based - conceptual)
def has_role(required_roles: list[str]):
    def role_checker(api_key: str = Depends(get_api_key)):
        user_roles = VALID_API_KEYS[api_key]["roles"]
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return True
    return role_checker

# 3. Rate Limiting (Simple in-memory, per-key)
# In a production environment, use a distributed rate limiter (e.g., Redis-based)
RATE_LIMIT_PER_MINUTE = 5
api_key_request_counts: Dict[str, Dict[int, int]] = defaultdict(lambda: defaultdict(int)) # {api_key: {minute: count}}

def rate_limit_checker(api_key: str = Depends(get_api_key)):
    current_minute = int(time.time() / 60)
    api_key_request_counts[api_key][current_minute] += 1

    # Clean up old minutes (optional, but good for long-running services)
    for minute in list(api_key_request_counts[api_key].keys()):
        if minute < current_minute - 1: # Keep current and last minute
            del api_key_request_counts[api_key][minute]

    if api_key_request_counts[api_key][current_minute] > RATE_LIMIT_PER_MINUTE:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Max {RATE_LIMIT_PER_MINUTE} requests per minute.",
        )
    return True

# --- API Models ---
class TaskRequest(BaseModel):
    task_description: str
    context: Optional[str] = None # e.g., relevant code snippets, conversation history
    file_paths: Optional[list[str]] = None # e.g., files to consider for the task

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[str] = None
    error: Optional[str] = None
    timestamp: float

# Initialize core components (conceptual)
# resource_manager = ResourceManager(config) # Assuming config is loaded globally or passed
# tool_interface = ToolInterface(config)
# orchestrator = Orchestrator(config, resource_manager, tool_interface)

# --- API Endpoints ---
@app.post("/run_task", response_model=TaskResponse, dependencies=[Depends(has_role(["user"])), Depends(rate_limit_checker)])
async def run_task(request: TaskRequest):
    """
    Submits a programming task to the Tanuki-Programmer for execution.
    Requires 'user' role and adheres to rate limits.
    """
    task_id = f"task_{int(time.time())}" # Simple unique ID for demonstration
    print(f"Received task {task_id}: {request.task_description}")

    # Simulate task processing
    # In a real implementation, this would call the orchestrator:
    # try:
    #     actual_result = await orchestrator.execute_task(
    #         request.task_description,
    #         context=request.context,
    #         file_paths=request.file_paths
    #     )
    #     status = "completed"
    #     result_content = actual_result
    #     error_content = None
    # except Exception as e:
    #     status = "failed"
    #     result_content = None
    #     error_content = str(e)

    # Simulated response
    simulated_output = f"""
Task: "{request.task_description}"
Context: {request.context if request.context else 'None'}
Files: {', '.join(request.file_paths) if request.file_paths else 'None'}

---
Simulated Tanuki-Programmer Output:

Analyzing task requirements...
Breaking down into sub-tasks...
Generating code for main logic...
Running tests...
Refactoring for production quality...

Task completed successfully!
(This is a simulated response. Actual output will vary based on the task and Tanuki-Programmer's capabilities.)
    """
    status = "completed"
    result_content = simulated_output
    error_content = None

    return TaskResponse(
        task_id=task_id,
        status=status,
        result=result_content,
        error=error_content,
        timestamp=time.time()
    )

@app.get("/health", dependencies=[Depends(get_api_key)]) # Health check also requires API key
async def health_check():
    """
    Health check endpoint to verify API is running. Requires API key.
    """
    return {"status": "ok", "message": "Tanuki-Programmer API is healthy."}

if __name__ == "__main__":
    import uvicorn
    # To run this API locally for testing:
    # uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)
