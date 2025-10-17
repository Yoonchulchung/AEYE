from langchain.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


class AEYE_Langchain_Model:
    
    def __init__(self):
    
        self.prompt = ChatPromptTemplate.from_template(
            """당신은 신중한 한국어 조교입니다. 답변은 한국어로 번역해서 답변하세요.
            아래 컨텍스트만 사용해 질문에 답하세요. 모르면 모른다고 하세요.
            간결하고 정확하게 답하고, 필요하면 근거(출처/페이지)를 문장 끝에 소괄호로 표기하세요.
            

            [컨텍스트]
            {context}

            [질문]
            {question}
            """
            )
        
        self.llm = ChatOllama(
            model="llama3",
            temperature=0,
        )
        
    def get_prompt(self, ):
        return self.prompt
    
    def get_llm(self, ):
        return self.llm