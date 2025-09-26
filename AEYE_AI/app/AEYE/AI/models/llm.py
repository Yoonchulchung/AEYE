
from AEYE.AI.registry import llm_register


@llm_register.register("LLaMA2")
class LLaMA2:
    
    def __init__(self, ):
        from langchain_community.chat_models import ChatOllama
        self.llm = ChatOllama(model="llama2", temperature=0.2)
        
    def get_model(self):
        return self.llm