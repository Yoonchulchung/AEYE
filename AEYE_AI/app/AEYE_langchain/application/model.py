from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


class AEYE_Langchain_Model:
    
    def __init__(self, cfg):
    
        self.cfg = cfg
        self.prompt = ChatPromptTemplate.from_template(self.cfg.prompt)
        
        self.llm = ChatOllama(
            model="llama3",
            temperature=self.cfg.temperature,
        )
        
    def get_prompt(self, ):
        return self.prompt
    
    def get_llm(self, ):
        return self.llm