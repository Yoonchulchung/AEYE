import os
from typing import Callable, List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_postgres.vectorstores import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter


class AEYE_Langchain_preprocess:
    
    def __init__(
        self, 
        vs : PGVector, 
        chunk_size : int = 1000, 
        chunk_overlap : int = 100,
        logger : Callable = None
        ):
        self.splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,         
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
        )
        
        self.vs = vs
        self.logger = logger
        
    def _load_pdf(self, pdf_path) -> List[Document]:
        
        if not os.path.exists(pdf_path):
            raise ValueError(f"Wrong path : {pdf_path}")
        
        loader = PyPDFLoader(pdf_path)
        return loader.load()
    

    def _get_chunk_from_text(self, pdf_file : List[Document]) -> List[str]:
        
        if not isinstance(pdf_file, List[Document]):
            raise ValueError(f"Wrong file type : {type(pdf_file)}")
        
        return self.splitter.split_text(pdf_file)

    def _insert_to_database(self, docs) -> None:
        self.vs.add_documents(docs)
    
    def add_pdf(self, pdf_file : str):
        
        self.logger(f"adding {pdf_file} to pgvector...")
        
        pdf_text = self._load_pdf(pdf_file)
        text = self._get_chunk_from_text(pdf_text)
        self._insert_to_database(text)
        
        self.logger(f"succeed to add {pdf_file}")
        