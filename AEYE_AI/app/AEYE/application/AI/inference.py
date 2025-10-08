import torch
import torch.nn as nn
from langchain_core.prompts import ChatPromptTemplate


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
    
    def __init__(self, octdl_model, llm_model, cfg):
        
        super().__init__()
        self.cfg = cfg
        
        self.vision_model = octdl_model
        self.llm_model = llm_model
        
        self.labels = self.cfg.Vision_AI.labels
        
        self.prompt = ChatPromptTemplate.from_messages([
                ("system", "너는 한국인 의사야. 한국어로 질병 치료 방법을 설명해야 해. 규칙 외에는 설명하지 마.\
                            규치: \
                            1.입력 용어에 대한 치료 방법 설명.\
                            2.어떤 약을 사용하면 좋을지 나열. \
                            3.수술이 필요한가 설명. "),
                ("human", "{question}")
            ])
    
    def _vision_inference(self, img):
        
        with torch.no_grad():
            pred = self.vision_model(img)
            probs = torch.softmax(pred, dim=1)          
            top_prob, top_idx = probs.max(dim=1)
            pred_label = self.labels[top_idx.item()]
            
        return pred_label
    
    def _llm_inference(self, pred):
                
        chain = self.prompt | self.llm_model
        return chain.invoke({"question": f"{pred}의 진료 방법은 뭐야."}).content
    
    
    def inference(self, img):
        
        result = {}
        pred = self._vision_inference(img)
        llm_result = self._llm_inference(pred)
        
        result["pred"] = pred
        result["llm_result"] = llm_result
        return result
        
    def forward(self, img):
        return self.inference(img)