import os
import re
from abc import ABC, abstractmethod
from typing import Callable, List

from langchain.text_splitter import SpacyTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader, UnstructuredPDFLoader
from langchain_core.documents import Document
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_postgres.vectorstores import PGVector


class AEYE_Langchain_Insert(ABC):
    '''
    
    '''
    @abstractmethod
    def add_pdf(self, pdf_path: str):
        '''
        
        '''
        raise NotImplementedError

class Langchain_Insert(AEYE_Langchain_Insert):
    
    def __init__(
        self, 
        vs : PGVector, 
        chunk_size : int = 1000, 
        chunk_overlap : int = 100,
        logger : Callable = None
        ):
        
        self.splitter = SpacyTextSplitter(chunk_size=chunk_size,
                                          chunk_overlap=chunk_overlap)
        self.loader = UnstructuredPDFLoader
        self.simple_loader = PyMuPDFLoader
        
        self.vs = vs
        self.logger = logger
        
    def _preprocess_pdf(self, pdf_path) -> str:
        '''
        PDF 파일 이름을 제목으로 변화합니다.
        
        ex :) Attention_is_all_you_need.pdf
        '''
        
        loader = self.simple_loader(pdf_path)
        documents = loader.load()
        
        metadata = documents[0].metadata
        pdf_title = metadata.get('title')
        pdf_author = metadata.get('author')
        
        if not pdf_title and not pdf_author:
            
            first_page_text = documents[0].page_content
            #llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
            llm = ChatOllama(
            model="llama3",
            temperature=0,
            )
            parser = JsonOutputParser()
            prompt = """
            You are an expert academic researcher skilled at parsing document information.
            Your task is to extract the main title and all authors from the text of the first page of a research paper provided below.

            Follow these rules carefully:
            1. The title is usually the largest, most prominent text at the top.
            2. Extract all author names. If there are multiple authors, include all of them.
            3. Format your response as a valid JSON object with two keys: "title" and "authors".
            4. The value for "title" must be a string.
            5. The value for "authors" must be a list of strings. If no authors are found, return an empty list [].
            6. Do NOT add any introductory text, explanations, or markdown formatting like ```json. Your response must be ONLY the raw JSON object.

            ---
            DOCUMENT TEXT:
            {first_page_text}
            ---

            JSON OUTPUT:
            """
            
            prompt = ChatPromptTemplate.from_template(template=prompt)
            
            chain = prompt | llm | parser
            result = chain.invoke({"first_page_text": first_page_text})
            print(result)
            
            pdf_title = result["title"]
            pdf_author = result["authors"]
            
        directory = os.path.dirname(pdf_path)
        
        new_filename = pdf_title.replace(" ", "_")
        new_pdf_path = os.path.join(directory, new_filename) + ".pdf"
        return new_pdf_path, pdf_author
        
    def _chunk_from_pdf(self, pdf_path) -> List[Document]:
        
        loader = self.loader(pdf_path, 
                             mode="paged", 
                             strategy="hi_res")
        
        pdf_file = loader.load()
    
        return self.splitter.split_documents(pdf_file)
        
    def _preprocess_chunks(self, documents : List[str], pdf_author) -> List[str]:
        '''
        아래 형식에 맞춰 메타 데이터를 만듭니다.
        
        metadata={
            'source': '저장 위치',
            'page': 0,
            'title': 'pdf 제목',
            'language': 'PDF 언어',
            'author': '문서의 저자 이름', 
            'published_date': '문서가 생성된 날짜와 시간',
            'doi': '디지털 학술 논문에 부여되는 고유 식별 번호',
            'keywords': '문서의 주제나 핵심 내용을 나타내는 키워드'
        }
        '''
        
        for doc in documents:
                        
            # 문장 중간의 불필요한 줄바꿈을 공백으로 변환
            doc.page_content = re.sub(r'\n\n(?!\n\n)', ' ', doc.page_content)
        
            # 여러 개의 공백을 하나로 축소
            doc.page_content = re.sub(r' +', ' ', doc.page_content)

            # 페이지 번호 제거
            lines = doc.page_content.strip().split('\n')
            if lines[0].strip().isdigit():
                doc.page_content = '\n'.join(lines[1:])
            
            if lines[-1].strip().isdigit():
                doc.page_content = '\n'.join(lines[:-1])
            
            pattern = r'^\s*[-~]?\s*p?\.?\s*\d+\s*[-~]?\s*$'
            if re.fullmatch(pattern, lines[0].strip(), re.IGNORECASE):
                doc.page_content = lines[1:]
            
            # 테이블인 경우
            
            # 이미지인 경우
            
            doc.metadata = self._metadata(doc.metadata, pdf_author)
            
            print("==")
            print(doc.metadata, pdf_author)
            print("==")
        return documents
        
    def _metadata(self, doc_metadata, pdf_author):
        metadata={
            'source': doc_metadata["source"],
            'page': doc_metadata["page_number"],
            'title': doc_metadata["filename"],
            'language' : doc_metadata["languages"],
            'author': pdf_author, 
            'published_date': '문서가 생성된 날짜와 시간',
            'keywords': '문서의 주제나 핵심 내용을 나타내는 키워드'
        }
        
        return metadata
        
    def _insert_to_database(self, docs) -> None:
        self.vs.add_documents(docs)
        
    
    def add_pdf(self, pdf_path : str):
        
        if not os.path.exists(pdf_path):
            raise ValueError(f"Wrong path : {pdf_path}")
        
        
        self.logger(f"adding {pdf_path} to pgvector...")
        pdf_path, pdf_author = self._preprocess_pdf(pdf_path)
        

        # pdf_chunk = self._chunk_from_pdf(pdf_path)
        # text = self._preprocess_chunks(pdf_chunk, pdf_author)        
        
        #self._insert_to_database(text)
        
        #self.logger(f"succeed to add {pdf_path}")