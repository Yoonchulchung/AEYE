from langchain.vectorstores import PGVector
from database import vectorstore

class AEYE_Langchain_DB:
    
    def __init__(self):
        self.vectorstore : PGVector = vectorstore
        
        self.retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 4, "fetch_k": 20, "lambda_mult": 0.5},
        )
    
    def get_retriever(self, ):
        return self.retriever
    
    def get_vectorstore(self, ):
        return self.vectorstore