from typing import Callable, Dict


class Registry:
    def __init__(self):
        self._map: Dict[str, Callable] = {}

    def register(self, name: str):
        def _wrap(cls_or_fn):
            self._map[name] = cls_or_fn
            return cls_or_fn
        return _wrap

    def get(self, model_name: str):
        
        if not model_name in self.list():
            raise ValueError(f"[{model_name}] is not registered. available models : {self.list()}")
        else:
            return self._map[model_name]

    def list(self):
        return list(self._map.keys())
    
vlm_register = Registry()
llm_register = Registry()
vision_register = Registry()

