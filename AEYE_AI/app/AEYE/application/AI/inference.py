import torch
import torch.nn as nn

from abc import abstractmethod
from PIL import Image

class IInference(nn.Module):
    '''
    AEYE AI 서버의 AI 추론을 담당합니다.
    '''
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    
    @abstractmethod
    def _vision_infer(self, img: Image.Image) -> str:
        '''
        OCT 모델을 이용하여 분류를 합니다.
        '''
        
        raise NotImplementedError
        
    @abstractmethod
    def _llm_infer(self, pred: str) -> str:
        '''
        RAG 기반 LLM 추론을 합니다. 
        '''
        
        raise NotImplementedError
    
    def forward(self, img : Image.Image):
        
        cls_output = self._vision_infer(img)
        llm_output = self._llm_infer(cls_output)
        
        result = {
            "cls_output" : cls_output,
            "llm_output" : llm_output,
        }
        
        return result
    

class InferenceGPU(IInference):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    
class InferenceGPU(nn.Module):
    
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError("AEYE_Inference is not initialized yet")
        return cls._instance
    
    def __init__(self, octdl_model, llm_model, cfg, langchain_search):
        
        super().__init__()
        self.cfg = cfg
        
        self.vision_model = octdl_model
        self.llm_model = llm_model
        
        self.labels = self.cfg.Vision_AI.labels
        self.langchain_search = langchain_search
    
    def _vision_inference(self, img):
        
        with torch.no_grad():
            pred = self.vision_model(img)
            probs = torch.softmax(pred, dim=1)          
            top_prob, top_idx = probs.max(dim=1)
            pred_label = self.labels[top_idx.item()]
            
        return pred_label
    
    def _llm_inference(self, pred):
        return self.langchain_search.search(f"{pred}의 진료 방법은 뭐야.")