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
    
    def __init__(self, octdl_model, llm_model):
        
        super().__init__()
        self.vision_model = octdl_model
        self.llm_model = llm_model
        
        self.labels = [
                "Age-related Macular Degeneration (AMD)",
                "Diabetic Macular Edema (DME)",
                "Epiretinal Membrane (ERM)",
                "Normal (NO)",
                "Retinal Artery Occlusion (RAO)",
                "Retinal Vein Occlusion (RVO)",
                "Vitreomacular Interface Disease (VID)",
            ]
        
        self.prompt = ChatPromptTemplate.from_messages([
                ("system", "You are helpful assistant"),
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
        return chain.invoke({"question": f"How patient should handle with {pred}"}).content
    
    
    def inference(self, img):
        
        pred = self._vision_inference(img)
        llm_result = self._llm_inference(pred)
        
        return llm_result
        
    def forward(self, img):
        return self.inference(img)