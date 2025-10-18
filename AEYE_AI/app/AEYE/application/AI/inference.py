import torch
import torch.nn as nn


class AEYE_Inference(nn.Module):
    
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
    
    def _inference(self, img):
        
        result = {}
        pred = self._vision_inference(img)
        llm_result = self._llm_inference(pred)
        
        result["pred"] = pred
        result["llm_result"] = llm_result
        return result
        
    def forward(self, img):
        return self._inference(img)