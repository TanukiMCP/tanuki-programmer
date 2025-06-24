import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .core.resource_management import list_available_adapters

app = FastAPI()

VLLM_URL = os.environ.get("VLLM_URL", "http://localhost:8000")

class PromptRequest(BaseModel):
    prompt: str
    adapter: str | None = None

@app.post("/generate")
async def generate(request: PromptRequest):
    model_to_use = request.adapter
    if model_to_use:
        if model_to_use not in list_available_adapters():
            raise HTTPException(status_code=400, detail=f"Adapter '{model_to_use}' not available.")
    else:
        model_to_use = "deepseek-ai/DeepSeek-Coder-V2-Lite"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{VLLM_URL}/v1/completions",
                json={
                    "model": model_to_use,
                    "prompt": request.prompt,
                    "max_tokens": 150,
                    "temperature": 0.7,
                },
                timeout=60.0,
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"Error communicating with vLLM: {exc}")
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)

@app.get("/adapters")
def get_adapters():
    """Returns a list of available LoRA adapters."""
    return {"adapters": list_available_adapters()}

@app.get("/")
def read_root():
    return {"message": "Tanuki Orchestrator is running"} 