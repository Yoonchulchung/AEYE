from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_postgres.vectorstores import PGVector


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
    
    def __init__(self, vectorstore : PGVector):
        
        self.vectorstore = vectorstore
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
        self.retriever = self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 4, "fetch_k": 20, "lambda_mult": 0.5},
        )
        
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

        chain = self.prompt | self.llm | StrOutputParser()
        return chain.invoke({"context": context_text, "question": question})