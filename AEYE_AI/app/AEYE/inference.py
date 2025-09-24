import numpy as np
import cv2
from langchain.llms import OpenAI, HuggingFaceHub
from langchain.chains import RetrievalQA

from AEYE.AI.models.octdl import generate_model

class AEYE_Inference():
    
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
        
        self.vision_model = octdl_model
        self.llm_model = llm_model
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.my_vectorstore.as_retriever()
        )
    
    def _vision_inference(self, img):
        img = _image_preprocessing(img)

        pred = self.vision_model(img)
        
        return pred
    
    def _llm_inference(self, pred):
        
        return self.qa_chain.run(f"{pred}를 진료하는 방법을 설명해줘")
        
        
    def inference(self, img):
        
        pred = self._vision_inference(img)
        llm_result = self._llm_inference(pred)
        
        return llm_result
        

def _image_preprocessing(img):
    img = cv2.resize(img,(224,224))
    img = np.reshape(img,[1,224,224,3])
    img = 1.0*img/255

    return img