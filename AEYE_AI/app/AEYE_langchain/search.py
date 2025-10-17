from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.vectorstores.base import VectorStoreRetriever


class AEYE_langchain_search:
        
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError("AEYE langchain search is not initialized yet")
        return cls._instance
    
    def __init__(self, 
                 llm,
                 retriever: VectorStoreRetriever, 
                 prompt : ChatPromptTemplate,
                 ):
        
        self.llm = llm
        self.prompt = prompt
        self.retriever = retriever
        
        self.chain = self.prompt | self.llm | StrOutputParser()
        
    def _format_query(self, text: str) -> str:
        return f"query: {text}"

    def _make_context_string(
        self,
        docs,
        max_chars: int = 2000,
    ) -> str:

        parts, total = [], 0
        for d in docs:
            chunk = d.page_content.strip()
            if not chunk:
                continue
            if total + len(chunk) > max_chars:
                break
            label = []
            if "source" in d.metadata:
                label.append(str(d.metadata["source"]))
            if "page" in d.metadata:
                label.append(f"p.{d.metadata['page']}")
            prefix = f"[{' | '.join(label)}]\n" if label else ""
            parts.append(prefix + chunk)
            total += len(chunk)
        return "\n\n---\n\n".join(parts)
    
    def search(self, question : str) -> str:
        
        q = self._format_query(question)
        
        docs = self.retriever.get_relevant_documents(q)
        context_text = self._make_context_string(docs, max_chars=2000)

        return self.chain.invoke({"context": context_text, "question": question})
    