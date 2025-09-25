import gc
from typing import Any, Callable
from langchain_community.llms import OpenAI, HuggingFaceHub
from AEYE.AI.models.octdl import generate_model
import torch


class ModelLoaderInterface:
    
    def get_model(self, model_name, gpu_id):
        raise NotImplemented
    

class GPUModelLoader(ModelLoaderInterface):
    # Only GPU Load is allowed

    def __init__(self, 
                 cfg,
                 free_mem_threshold : float = 2.0, # Bytes
                 vision_register : Callable = None,
                 vlm_register : Callable = None,
                 logger : Callable = None,
                 ):
        super().__init__()
        
        self.cfg = cfg
        self.free_mem_threshold = free_mem_threshold
    
        self.vlm_register = vlm_register
        
        self.llm_list = ["gpt-4o-mini"]
        self.vision_list = ["octdl", ]
        
        self.logger = logger
        if not torch.cuda.is_available():
            raise ValueError("GPU is not available")
        
    def _check_mem_ok(self, gpu_id) -> bool:
        
        try:
            free_b, total_b = torch.cuda.mem_get_info()
        except Exception:
            props = torch.cuda.get_device_properties(gpu_id)
            total_b = props.total_memory
            free_b = max(0, total_b - torch.cuda.memory_reserved(gpu_id) - torch.cuda.memory_allocated(gpu_id))
            self.logger(free_b)
        return free_b >= self.free_mem_threshold
    
    def _load_vlm(self, model_name, gpu_id):
        model = self.vlm_register.get(model_name)
        model = model(self.cfg, "cuda")
        return model
        
    def _load_vision(self, model_name, gpu_id):
        
        model = generate_model(self.cfg)
        return model.to('cuda').eval()
        
    def _load_llm(self, model_name : str, gpu_id):
        
        # We are going to use langchain
        if model_name.lower() == "gpt-4o-mini":
            return OpenAI(model="gpt-4o-mini")  

    
    def get_model_list(self):
        return self.vlm_register.list()
        
    async def get_model(self, model_name, gpu_id):
        
        self.logger(f"{model_name} is loading...")
        in_vision = model_name in self.vision_list
        in_vlm    = model_name in self.vlm_register.list()
        in_llm    = model_name in self.llm_list
        
        if not (in_vision or in_vlm or in_llm):
            raise ValueError(
                f"Unknown model_name: '{model_name}'."
            )

        assert gpu_id in list(range(torch.cuda.device_count())), \
        f"gpu_id should be between 0 and {torch.cuda.device_count() - 1}"

        try:
            if in_vlm:
                model = self._load_vlm(model_name, gpu_id)
            elif in_vision :
                model = self._load_vision(model_name, gpu_id)
            else:
                model = self._load_llm(model_name, gpu_id)
            
            if model is None:
                raise KeyError(f"Registry returned None for '{model_name}'")

            if not self._check_mem_ok(gpu_id):
                del model
                gc.collect()
                torch.cuda.empty_cache()
        except Exception as e:
            try:
                if model is not None:
                    del model
                gc.collect()
                torch.cuda.empty_cache()
            finally:
                raise RuntimeError(f"Failed to instantiate '{model_name}' on cuda:{gpu_id}: {e}") from e
        
        self.logger(f"{model_name} is loaded!")
        return model