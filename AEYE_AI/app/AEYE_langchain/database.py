from langchain.vectorstores import PGVector

from database import vectorstore


class AEYE_Langchain_DB:
    
    def __init__(self, cfg):
        self.vectorstore : PGVector = vectorstore
        self.cfg = cfg
        self.retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": self.cfg.retriever_k, 
                           "fetch_k": self.cfg.retriever_fetch_k, 
                           "lambda_mult": self.cfg.retriever_mult},
        )
    
    def get_retriever(self, ):
        return self.retriever
    
    def get_vectorstore(self, ):
        return self.vectorstore