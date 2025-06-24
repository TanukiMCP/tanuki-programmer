import psutil
import collections
import threading
import time
from typing import Dict, Any, Optional, Tuple
from peft import PeftModel # New import for handling LoRA adapters
from transformers import AutoModelForCausalLM, AutoTokenizer # Needed for loading base model if not passed in
from transformers.utils.quantization_config import BitsAndBytesConfig # For BitsAndBytesConfig in test
import torch # Needed for device management and data types
import gc # For garbage collection

class ResourceMonitor:
    """
    Monitors system resources, including system RAM and a placeholder for VRAM.
    """
    def __init__(self):
        pass

    def get_system_ram_usage(self) -> Dict[str, float]:
        """
        Retrieves current system RAM usage.

        Returns:
            Dict[str, float]: Dictionary with 'total', 'available', 'used', 'percent' in GB.
        """
        mem = psutil.virtual_memory()
        total_gb = mem.total / (1024**3)
        available_gb = mem.available / (1024**3)
        used_gb = mem.used / (1024**3)
        percent = mem.percent
        return {
            "total_gb": round(total_gb, 2),
            "available_gb": round(available_gb, 2),
            "used_gb": round(used_gb, 2),
            "percent": percent
        }

    def get_vram_usage(self) -> Dict[str, float]:
        """
        Placeholder for VRAM usage retrieval.
        Actual implementation would require libraries like pynvml (NVIDIA) or specific AMD tools.

        Returns:
            Dict[str, float]: Dictionary with 'total_gb', 'used_gb', 'percent'.
        """
        # In a production environment, this would integrate with NVIDIA (pynvml)
        # or AMD (rocm-smi/amdgpu) monitoring tools.
        # Example with pynvml:
        # from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo, nvmlShutdown
        # try:
        #     nvmlInit()
        #     handle = nvmlDeviceGetHandleByIndex(0) # Assuming single GPU
        #     info = nvmlDeviceGetMemoryInfo(handle)
        #     total_mb = info.total / (1024**2)
        #     used_mb = info.used / (1024**2)
        #     percent = (used_mb / total_mb) * 100 if total_mb > 0 else 0
        #     return {"total_gb": total_mb / 1024, "used_gb": used_mb / 1024, "percent": percent}
        # except Exception:
        #     return {"total_gb": 0.0, "used_gb": 0.0, "percent": 0.0}
        # finally:
        #     try: nvmlShutdown()
        #     except Exception: pass

        print("ResourceMonitor: VRAM monitoring is a placeholder. Requires specific GPU libraries.")
        return {
            "total_gb": 16.0, # Simulated total VRAM
            "used_gb": 2.5,  # Simulated used VRAM
            "percent": (2.5 / 16.0) * 100
        }

class AdapterLoaderUnloader:
    """
    Dynamically loads and unloads LoRA adapters, integrating with an LRU cache
    and enforcing memory budgets.
    """
    def __init__(self,
                 base_model: Any, # Expecting a loaded base model (can be AutoModelForCausalLM or a mock)
                 base_tokenizer: Any, # Expecting a loaded base tokenizer (can be AutoTokenizer or a mock)
                 max_cache_size: int = 5,
                 vram_budget_gb: float = 10.0):
        self.base_model = base_model
        self.base_tokenizer = base_tokenizer
        self.adapter_cache = collections.OrderedDict() # Stores {adapter_path: PeftModel instance}
        self.max_cache_size = max_cache_size
        self.vram_budget_gb = vram_budget_gb
        self.current_vram_usage_gb = 0.0 # Tracks simulated VRAM usage by loaded adapters
        self.lock = threading.Lock() # For thread-safe cache operations

    def _get_adapter_size_gb(self, adapter_path: str) -> float:
        """
        Estimates the size of an adapter in GB.
        IMPORTANT: This is a placeholder. In a production system, this method MUST
        be replaced with an accurate implementation that:
        1. Reads the actual file size of the adapter on disk.
        2. Or, uses metadata from the PEFT config to estimate memory footprint.
        For demonstration, we use a heuristic based on adapter name.
        """
        # Simulate varying adapter sizes for testing LRU and budget enforcement
        if "large" in adapter_path:
            return 0.5 # e.g., 500MB
        elif "medium" in adapter_path:
            return 0.2 # e.g., 200MB
        elif "small" in adapter_path:
            return 0.1 # e.g., 100MB
        elif "tiny" in adapter_path:
            return 0.05 # e.g., 50MB
        elif "extra_large" in adapter_path:
            return 1.0 # e.g., 1GB
        else:
            return 0.3 # Default size if no keyword matches (300MB)

    def _load_adapter_from_disk(self, adapter_path: str) -> PeftModel:
        """
        Loads a LoRA adapter from the specified path and attaches it to the base model.
        """
        print(f"AdapterLoaderUnloader: Loading adapter from {adapter_path}...")
        # Ensure the base model is in evaluation mode before loading adapter
        self.base_model.eval()
        # Load the PEFT model. This attaches the adapter to the base_model.
        # The returned PeftModel instance is essentially the base_model with the adapter active.
        adapter_model = PeftModel.from_pretrained(self.base_model, adapter_path)
        print(f"AdapterLoaderUnloader: Adapter loaded from {adapter_path}.")
        return adapter_model

    def load_adapter(self, adapter_path: str) -> PeftModel:
        """
        Loads an adapter into memory, using the LRU cache.
        If the cache is full, the least recently used adapter is unloaded.
        Enforces VRAM budget.

        Args:
            adapter_path (str): The file system path to the LoRA adapter.

        Returns:
            PeftModel: The base model with the specified LoRA adapter loaded and active.
        """
        with self.lock:
            if adapter_path in self.adapter_cache:
                # Move to end to mark as recently used
                adapter = self.adapter_cache.pop(adapter_path)
                self.adapter_cache[adapter_path] = adapter
                print(f"AdapterLoaderUnloader: Adapter '{adapter_path}' already loaded and moved to front of LRU.")
                return adapter

            estimated_size_gb = self._get_adapter_size_gb(adapter_path)

            # Check memory budget before loading
            if (self.current_vram_usage_gb + estimated_size_gb) > self.vram_budget_gb:
                print(f"AdapterLoaderUnloader: VRAM budget exceeded ({self.current_vram_usage_gb + estimated_size_gb:.2f}GB > {self.vram_budget_gb:.2f}GB). Attempting to unload LRU adapters.")
                while (self.current_vram_usage_gb + estimated_size_gb) > self.vram_budget_gb and len(self.adapter_cache) > 0:
                    lru_adapter_path, _ = self.adapter_cache.popitem(last=False) # Get and remove LRU
                    lru_adapter_size = self._get_adapter_size_gb(lru_adapter_path)
                    # For PEFT, 'unloading' means removing from our cache and potentially deactivating.
                    # The actual memory might not be freed until Python's GC runs or explicitly cleared.
                    # Here, we just update our simulated usage.
                    self.current_vram_usage_gb -= lru_adapter_size
                    print(f"AdapterLoaderUnloader: Unloaded LRU adapter '{lru_adapter_path}' (size: {lru_adapter_size:.2f}GB). Current VRAM usage: {self.current_vram_usage_gb:.2f}GB.")
                    # Optional: Explicitly clear memory if needed, e.g., torch.cuda.empty_cache()
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
                    gc.collect()
                
                if (self.current_vram_usage_gb + estimated_size_gb) > self.vram_budget_gb:
                    raise MemoryError(f"Cannot load adapter '{adapter_path}'. VRAM budget still exceeded even after unloading LRU adapters. Required: {estimated_size_gb:.2f}GB, Available: {self.vram_budget_gb - self.current_vram_usage_gb:.2f}GB.")

            # Load the actual adapter
            print(f"AdapterLoaderUnloader: Loading adapter '{adapter_path}' (estimated size: {estimated_size_gb:.2f}GB)...")
            adapter_object = self._load_adapter_from_disk(adapter_path)
            self.adapter_cache[adapter_path] = adapter_object
            self.current_vram_usage_gb += estimated_size_gb
            print(f"AdapterLoaderUnloader: Adapter '{adapter_path}' loaded. Current VRAM usage: {self.current_vram_usage_gb:.2f}GB.")

            # Enforce max cache size
            while len(self.adapter_cache) > self.max_cache_size:
                lru_adapter_path, _ = self.adapter_cache.popitem(last=False) # Get and remove LRU
                lru_adapter_size = self._get_adapter_size_gb(lru_adapter_path)
                self.current_vram_usage_gb -= lru_adapter_size
                print(f"AdapterLoaderUnloader: Unloaded LRU adapter '{lru_adapter_path}' due to cache size limit (size: {lru_adapter_size:.2f}GB). Current VRAM usage: {self.current_vram_usage_gb:.2f}GB.")
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                gc.collect()
            
            return adapter_object

    def unload_adapter(self, adapter_path: str):
        """
        Unloads a specific adapter from the cache.
        Note: For PEFT models, 'unloading' typically means deactivating the adapter
        or removing it from the base model's active adapters. Here, we simply remove
        it from our cache and update simulated VRAM. The actual PEFT model object
        might still exist in memory until Python's garbage collector runs.
        """
        with self.lock:
            if adapter_path in self.adapter_cache:
                adapter_size = self._get_adapter_size_gb(adapter_path)
                del self.adapter_cache[adapter_path]
                self.current_vram_usage_gb -= adapter_size
                print(f"AdapterLoaderUnloader: Unloaded adapter '{adapter_path}' (size: {adapter_size:.2f}GB). Current VRAM usage: {self.current_vram_usage_gb:.2f}GB.")
                # Optional: Explicitly clear memory if needed
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                gc.collect()
            else:
                print(f"AdapterLoaderUnloader: Adapter '{adapter_path}' not found in cache.")

    def get_loaded_adapters(self) -> Dict[str, Any]:
        """Returns the currently loaded adapters in the cache."""
        return dict(self.adapter_cache)

    def get_current_vram_usage_by_adapters(self) -> float:
        """Returns the simulated VRAM usage by loaded adapters."""
        return self.current_vram_usage_gb

# In a real implementation, this could be loaded from a config file
# or discovered from the filesystem.
AVAILABLE_LORA_ADAPTERS = [
    "tanuki-python-coder",
    # ... other 126 adapters would be listed here
]

def list_available_adapters():
    """Returns a list of available LoRA adapters."""
    return AVAILABLE_LORA_ADAPTERS

def get_adapter_path(adapter_name: str) -> str:
    """Returns the path to a LoRA adapter."""
    if adapter_name not in AVAILABLE_LORA_ADAPTERS:
        raise ValueError(f"Adapter {adapter_name} not found.")
    return f"/app/models/lora_adapters/{adapter_name}"

if __name__ == "__main__":
    # Test ResourceMonitor
    monitor = ResourceMonitor()
    print("--- Resource Monitor Test ---")
    ram_usage = monitor.get_system_ram_usage()
    print(f"System RAM Usage: {ram_usage['used_gb']:.2f}GB / {ram_usage['total_gb']:.2f}GB ({ram_usage['percent']:.2f}%)")
    vram_usage = monitor.get_vram_usage()
    print(f"Simulated VRAM Usage: {vram_usage['used_gb']:.2f}GB / {vram_usage['total_gb']:.2f}GB ({vram_usage['percent']:.2f}%)")

    # Test AdapterLoaderUnloader for 90 agents within 10.2GB budget
    print("\n--- Adapter Loader/Unloader Test (90 Agents, 10.2GB VRAM Budget) ---")
    
    # Simulate loading a base model and tokenizer for the AdapterLoaderUnloader
    # In a real scenario, these would be actual loaded objects from ModelTrainer.
    print("Simulating base model and tokenizer loading for AdapterLoaderUnloader...")
    try:
        # Dummy quantization config for simulation (corrected syntax)
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
        
        # Use a dummy model name for testing purposes, as we don't actually load it here.
        # The actual model loading would happen in ModelTrainer.
        # For this test, we just need a placeholder object that behaves like a model.
        class DummyModel:
            def eval(self):
                # print("DummyModel: eval() called.")
                pass
            def to(self, device):
                # print(f"DummyModel: moved to {device}.")
                return self
            def __call__(self, *args, **kwargs):
                # print("DummyModel: __call__ (inference) called.")
                return self
            def generate(self, *args, **kwargs):
                # print("DummyModel: generate called.")
                return "simulated generation"
            def push_to_hub(self, *args, **kwargs):
                # print("DummyModel: push_to_hub called.")
                pass
            def save_pretrained(self, *args, **kwargs):
                # print("DummyModel: save_pretrained called.")
                pass
            def add_adapter(self, adapter_name, adapter_config):
                # print(f"DummyModel: add_adapter called for {adapter_name}")
                pass
            def set_adapter(self, adapter_name):
                # print(f"DummyModel: set_adapter called for {adapter_name}")
                pass
            def disable_adapter(self, adapter_name):
                # print(f"DummyModel: disable_adapter called for {adapter_name}")
                pass


        class DummyTokenizer:
            def __call__(self, text, return_tensors="pt"):
                # print(f"DummyTokenizer: tokenizing '{text}'")
                return {"input_ids": torch.tensor([[1,2,3]]), "attention_mask": torch.tensor([[1,1,1]])}
            def save_pretrained(self, *args, **kwargs):
                # print("DummyTokenizer: save_pretrained called.")
                pass

        # Simulate the base model and tokenizer
        simulated_base_model = DummyModel()
        simulated_base_tokenizer = DummyTokenizer()

        # Set VRAM budget to 10.2GB as requested
        VRAM_BUDGET_GB = 10.2
        # Max cache size can be higher to allow more agents to stay in cache if budget allows
        MAX_CACHE_SIZE = 90 # Allow all 90 agents to be in cache if memory permits

        loader = AdapterLoaderUnloader(
            base_model=simulated_base_model,
            base_tokenizer=simulated_base_tokenizer,
            max_cache_size=MAX_CACHE_SIZE,
            vram_budget_gb=VRAM_BUDGET_GB
        )

        # Create dummy adapter directories for testing
        base_adapter_dir = "models/trained"
        import os
        os.makedirs(base_adapter_dir, exist_ok=True)

        # Simulate a PeftModel.from_pretrained call
        class MockPeftModel(PeftModel):
            def __init__(self, base_model, adapter_path):
                super().__init__(base_model, {}) 
                self.base_model = base_model
                self.adapter_path = adapter_path
                # print(f"MockPeftModel initialized for {adapter_path}")
            
            @classmethod
            def from_pretrained(cls, base_model, adapter_path, **kwargs):
                base_model.add_adapter(adapter_path, {})
                base_model.set_adapter(adapter_path)
                return cls(base_model, adapter_path)

            def eval(self):
                # print(f"MockPeftModel {self.adapter_path}: eval() called.")
                pass
            def to(self, device):
                # print(f"MockPeftModel {self.adapter_path}: moved to {device}.")
                return self
            def __call__(self, *args, **kwargs):
                # print(f"MockPeftModel {self.adapter_path}: __call__ (inference) called.")
                return self.base_model(*args, **kwargs)
            def generate(self, *args, **kwargs):
                # print(f"MockPeftModel {self.adapter_path}: generate called.")
                return self.base_model.generate(*args, **kwargs)

        # Patch PeftModel.from_pretrained for testing
        original_from_pretrained = PeftModel.from_pretrained
        PeftModel.from_pretrained = MockPeftModel.from_pretrained

        # Simulate 90 agents with varying sizes (mostly 30MB, some larger)
        agent_paths = []
        for i in range(90):
            if i % 10 == 0: # Every 10th agent is medium (200MB)
                agent_paths.append(os.path.join(base_adapter_dir, f"agent_{i}_medium"))
            elif i % 25 == 0: # Every 25th agent is large (500MB)
                agent_paths.append(os.path.join(base_adapter_dir, f"agent_{i}_large"))
            else: # Most agents are small (100MB)
                agent_paths.append(os.path.join(base_adapter_dir, f"agent_{i}_small"))
            # Create dummy directories for these agents
            os.makedirs(agent_paths[-1], exist_ok=True)

        print(f"Attempting to load {len(agent_paths)} agents with a VRAM budget of {VRAM_BUDGET_GB}GB...")
        loaded_count = 0
        total_loaded_size = 0.0
        for i, path in enumerate(agent_paths):
            try:
                loader.load_adapter(path)
                loaded_count += 1
                total_loaded_size = loader.get_current_vram_usage_by_adapters()
                print(f"  Loaded {os.path.basename(path)}. Current VRAM: {total_loaded_size:.2f}GB. Cache size: {len(loader.get_loaded_adapters())}")
            except MemoryError as e:
                print(f"  Failed to load {os.path.basename(path)}: {e}")
                break # Stop if budget is hit and no more can be loaded

        print(f"\n--- Summary ---")
        print(f"Total agents attempted to load: {len(agent_paths)}")
        print(f"Total agents successfully loaded into cache: {loaded_count}")
        print(f"Final VRAM usage by adapters: {loader.get_current_vram_usage_by_adapters():.2f}GB (Budget: {VRAM_BUDGET_GB}GB)")
        print(f"Final number of adapters in cache: {len(loader.get_loaded_adapters())}")
        
        # Demonstrate LRU behavior by accessing older agents
        print("\nDemonstrating LRU behavior by accessing older agents...")
        # Access agent 0 (should be oldest if all loaded)
        if loaded_count > 0:
            print(f"Accessing {os.path.basename(agent_paths[0])}...")
            loader.load_adapter(agent_paths[0]) # This will move it to the end of LRU
            print(f"Loaded Adapters (LRU updated): {list(loader.get_loaded_adapters().keys())[-5:]} (last 5)")

        # Attempt to load more if budget allows, to see if LRU kicks in again
        print("\nAttempting to load a few more agents to trigger LRU if needed...")
        for i in range(90, 95): # Try loading 5 more agents
            path = os.path.join(base_adapter_dir, f"agent_{i}_small")
            os.makedirs(path, exist_ok=True)
            try:
                loader.load_adapter(path)
                print(f"  Loaded {os.path.basename(path)}. Current VRAM: {loader.get_current_vram_usage_by_adapters():.2f}GB. Cache size: {len(loader.get_loaded_adapters())}")
            except MemoryError as e:
                print(f"  Failed to load {os.path.basename(path)}: {e}")
                break

        print(f"\nFinal VRAM usage by adapters: {loader.get_current_vram_usage_by_adapters():.2f}GB (Budget: {VRAM_BUDGET_GB}GB)")
        print(f"Final number of adapters in cache: {len(loader.get_loaded_adapters())}")

        # Restore original PeftModel.from_pretrained
        PeftModel.from_pretrained = original_from_pretrained

    except Exception as e:
        print(f"An error occurred during AdapterLoaderUnloader test: {e}")
        import traceback
        traceback.print_exc()

    print("\nAdapter loading/unloading demonstration complete.")
