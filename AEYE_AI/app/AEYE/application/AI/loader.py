import gc
from typing import Callable

import torch
from abc import abstractmethod


class ModelLoaderInterface:
    '''
    AEYE AI 서버의 AI 모델 담당입니다. 싱글턴으로 정의하세요. 
    AI 모델을 쉽게 변경하고 사용할 수 있도록 정의해주세요. 어떤 AI 모델을 요청할지 모르기 
    때문에 모델 로드, 사용, 변경 중에 시스템이 멈춰서는 안됩니다. 모델의 책임은 여기에 
    있습니다.
    
    AEYE AI 서버가 시작될 때 사용할 기본 AI 모델은 config에서 설정합니다. 
    '''
    
    @abstractmethod
    async def get_model(self, model_name) -> Callable:
        '''
        런타임에 AI 모델을 할당받을 수 있습니다. 시스템에 더 이상 모델을 추가시킬 수 없다면
        모델을 반환해주지 않아요. 
        
        요청한 모델의 성능을 평가합니다. 아래와 같은 정보가 출력될거에요.
            "Model running warmup..."
            "Model warmup completed!"
            "Model Name : [모델 이름] | Throughput : 128/s"
        '''
        raise NotImplementedError

    @abstractmethod
    def get_model_list(self) -> dict:
        '''
        사용 가능한 모델들을 확인할 수 있습니다. 반환 정보는 아래와 같아요.
        {
            "vision" : [],
            "llm" : [],
            "vlm" : [],
        }
        '''
        raise NotImplementedError
    
    @abstractmethod
    def get_llm(self) -> Callable:
        '''
        현재 기본으로 사용하고 있는 llm 모델의 인스턴스를 할당받을 수 있습니다. 시스템이
        더이상 모델을 추가시킬 수 없다면 모델을 반환해주지 않아요.
        
        요청한 모델의 성능을 평가합니다. 아래와 같은 정보가 출력될거에요.
            "Model running warmup..."
            "Model warmup completed!"
            "Model Name : [모델 이름] | Throughput : 128/s"
        '''
        raise NotImplementedError
    
    @abstractmethod
    def get_llm_name(self) -> str:
        '''
        현재 기본으로 사용하고 있는 llm 모델의 이름을 확인할 수 있습니다. 
        '''
        raise NotImplementedError
    
    @abstractmethod
    def get_vision(self) -> Callable:
        '''
        현재 기본으로 사용하고 있는 vision 모델의 인스턴스를를 할당받을 수 있습니다. 시스템이
        더이상 모델을 추가시킬 수 없다면 모델을 반환해주지 않아요.
        
        요청한 모델의 성능을 평가합니다. 아래와 같은 정보가 출력될거에요.
            "Model running warmup..."
            "Model warmup completed!"
            "Model Name : [모델 이름] | Throughput : 128/s"

        '''
        raise NotImplementedError
    
    @abstractmethod
    def get_vision_name(self) -> str:
        '''
        현재 기본으로 사용하고 있는 vision 모델의 이름을 확인할 수 있습니다. 
        '''
        raise NotImplementedError
    

class GPUModelLoader(ModelLoaderInterface):
    # Only GPU Load is allowed

    def __init__(self, 
                 cfg,
                 free_mem_threshold : float = 2.0, # Bytes
                 vision_register : Callable = None,
                 vlm_register : Callable = None,
                 llm_register : Callable = None,
                 logger : Callable = None,
                 ):
        super().__init__()
        
        self.cfg = cfg
        self.free_mem_threshold = free_mem_threshold
    
        self.vlm_register = vlm_register
        
        self.llm_list = llm_register
        self.vision_list = vision_register
        
        self.logger = logger
        if not torch.cuda.is_available():
            raise ValueError("GPU is not available")
    
    def _load_vlm(self, model_name):
        model = self.vlm_register.get(model_name)
        model = model(self.cfg, "cuda")
        return model
        
    def _load_vision(self, model_name):
        
        model_cls = self.vision_list.get(model_name)
        model_inst = model_cls(self.cfg)
        model = model_inst.get_model()
        return model.to('cuda').eval()
        
    def _load_llm(self, model_name : str):
        
        # We are going to use langchain
        model_cls = self.llm_list.get(model_name)
        model_inst = model_cls()
        return model_inst.get_model()

    
    def get_model_list(self):
        return self.vlm_register.list()
        
    async def get_model(self, model_name, gpu_id):
        
        self.logger(f"{model_name} is loading...")
        in_vision = model_name in self.vision_list.list()
        in_vlm    = model_name in self.vlm_register.list()
        in_llm    = model_name in self.llm_list.list()
        
        if not (in_vision or in_vlm or in_llm):
            raise ValueError(
                f"Unknown model_name: '{model_name}'.",
                f"Available model in vision : {self.vision_list.list()}",
                f"Available model in llm : {self.llm_list.list()}",
            )

        assert gpu_id in list(range(torch.cuda.device_count())), \
        f"gpu_id should be between 0 and {torch.cuda.device_count() - 1}"

        try:
            if in_vlm:
                model = self._load_vlm(model_name)
            elif in_vision :
                model = self._load_vision(model_name)
            else:
                model = self._load_llm(model_name)
            
            if model is None:
                raise KeyError(f"Registry returned None for '{model_name}'")

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