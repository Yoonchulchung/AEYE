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
from langchain_postgres.vectorstores import PGVector


class AEYE_Langchain_Insert(ABC):
    '''
    Vectorstore DB에 저장할 PDF 문서 처리를 관리합니다. 
    
    아래와 같은 파이프라인으로 문서를 처리합니다.
    PDF 전처리 -> 텍스트 추출 -> 텍스트 전처리 -> 청크 분할 -> DB 저장
    
    '''
    
    @abstractmethod
    def _preprocess_pdf(self, pdf_path):
        '''
        PDF 파일을 전처리합니다. PDF를 파싱하기 전 가벼운 PDF 파서 모델을 이용하여
        전처리를 진행합니다.
        
        먼저, PDF가 이미지 기반인지 확인합니다. OCR 사용 여부를 체크합니다.
        
        LLM 모델을 이용하여 파싱된 PDF 파일에서 아래와 같은 정보를 추출합니다.
        문서의 첫 페이지만을 이용합니다.
        - PDF 문서의 제목
        - PDF 문서의 카테고리
        - PDF 문서가 논문이라면, 저자명을 추출합니다.
        
        정갈된 전처리를 위해 추출된 PDF 제목을 파일 명으로 변경합니다.
        ex :) Attention_is_all_you_need.pdf
        '''
        raise NotImplementedError
    
    @abstractmethod
    def _get_text_from_pdf(self, pdf_path):
        '''
        PDF에서 텍스트를 추출합니다.
        
        표와 이미지를 따로 추출하여 관리합니다. 추출한 자리는 흔적을 남깁니다.
        
        이미지는 아래와 같은 방법으로 관리합니다.
        1. 이미지는 VLM을 이용해서 이미지를 설명하는 텍스트로 변환합니다.
        2. 이미지와 텍스트를 연결해서 검색할 때 찾을 수 있도록 합니다.
        
        Reference는 별도의 메타데이터에 분리합니다. Reference는 검색 정확도를
        하락시킬 수 있습니다.
        
        '''
        raise NotImplementedError
    
    @abstractmethod
    def _preprocess_text(self, txt):
        '''
        RAG 검색에 성능을 하락시키는 불필요한 내용을 제거하고 변경합니다.
        
        머리글/꼬리글 제거, 줄 바꿈 병합, 특수 문자 제거합니다.
        
        
        청크 레벨의 메타데이터와 문서 레벨의 메타데이터를 별도로 관리합니다.
        아래 형식에 맞춰 메타 데이터를 만듭니다.
        
        metadata={
            'source': '저장 위치',
            'page': 0,
            'title': 'pdf 제목',
            'language': 'PDF 언어',
            'author': '문서의 저자 이름', 
            'published_date': '문서가 생성된 날짜와 시간',
            'keywords': '청크의 주제나 핵심 내용을 나타내는 키워드'
        }
        '''
        
        raise NotImplementedError
    
    @abstractmethod
    def _get_chunk(self, text):
        '''
        
        '''
        raise NotImplementedError
        
    @abstractmethod
    def _insert_to_database(self, text):
        '''
        vectorstore DB에 저장합니다.
        '''
        raise NotImplementedError
    
    
    
    def add_pdf(self, pdf_path : str):
        
        if not os.path.exists(pdf_path):
            raise ValueError(f"Wrong path : {pdf_path}")
        
        self.logger(f"adding {pdf_path} to pgvector...")
        pdf_path = self._preprocess_pdf(pdf_path)
        
        # pdf_chunk = self._get_text_from_pdf(pdf_path)
        # text = self._preprocess_text(pdf_chunk, pdf_author)        
        #chunks = self._get_chunk(text)
        #self._insert_to_database(text)
        
        #self.logger(f"succeed to add {pdf_path}")

class Langchain_Insert(AEYE_Langchain_Insert):
    preprocess_pdf_prompt = """
    You are an expert academic researcher skilled at parsing document information.
    Your task is to extract the main title, all authors, and category from the text of the first page of a research paper provided below.

    Follow these rules carefully:
    1. The title is usually the largest, most prominent text at the top.
    2. Extract all author names. If there are multiple authors, include all of them.
    3. Format your response as a valid JSON object with three keys: "title", "authors", and "category".
    4. The value for "title" must be a string and lowercase.
    5. The value for "authors" must be a list of strings. If no authors are found, return an empty list [].
    7. The value for "category" mus be a string.
    6. Do NOT add any introductory text, explanations, or markdown formatting like ```json. Your response must be ONLY the raw JSON object.
    
    ---
    DOCUMENT TEXT:
    {first_page_text}
    ---

    JSON OUTPUT:
    """
    
    
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
        
        #llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
        self.llm = ChatOllama(model="llama3",
                              temperature=0)
        
        self.vs = vs
        self.logger = logger
        
        self.title = None
        self.author = None
        self.cateogy = None
        
        
    def _preprocess_pdf(self, pdf_path) -> str:
        
        loader = self.simple_loader(pdf_path, mode="page")
        documents = loader.load()
        
        metadata = documents[0].metadata
        pdf_title = metadata.get('title')
        pdf_author = metadata.get('author')
        pdf_category = metadata.get('category')
        
        first_page_text = self._preprocess_text(documents[0].page_content, "PyMu")
        
        if not pdf_title and not pdf_author and not pdf_category:
            
            parser = JsonOutputParser()
            prompt = ChatPromptTemplate.from_template(template=self.preprocess_pdf_prompt)
            
            chain = prompt | self.llm | parser
            result = chain.invoke({"first_page_text": first_page_text})
            
            pdf_title = result["title"]
            pdf_author = result["authors"]
            pdf_category = result["category"]  
        
        self.title = pdf_title
        self.author = pdf_author
        self.cateogy = pdf_category

        directory = os.path.dirname(pdf_path)
        new_filename = pdf_title.replace(" ", "_")
        
        new_path = os.path.join(directory, new_filename) + ".pdf"
        os.rename(pdf_path, new_path)
        
        return new_path
            
    def _get_text_from_pdf(self, pdf_path) -> List[Document]:
        
        loader = self.loader(pdf_path, 
                             mode="paged", 
                             strategy="hi_res")
        
        pdf_file = loader.load()
    
        return pdf_file
    
    def _preprocess_text(self, texts, mode):
        
        # 문장 중간의 불필요한 줄바꿈을 공백으로 변환
        if mode == "PyMu":
            texts = re.sub(r'\n(?!\n)', ' ', texts)
        else:
            texts = re.sub(r'\n\n(?!\n\n)', ' ', texts)

        # 여러 개의 공백을 하나로 축소
        texts = re.sub(r' +', ' ', texts)

        # 페이지 번호 제거
        lines = texts.strip().split('\n')
        if lines[0].strip().isdigit():
            texts = '\n'.join(lines[1:])
        
        if lines[-1].strip().isdigit():
            texts = '\n'.join(lines[:-1])
        
        pattern = r'^\s*[-~]?\s*p?\.?\s*\d+\s*[-~]?\s*$'
        if re.fullmatch(pattern, lines[0].strip(), re.IGNORECASE):
            texts = lines[1:]
        
        # 테이블인 경우
        
        # 이미지인 경우
        
        return texts
        
    def _metadata(self, doc_metadata):
        metadata={
            'source': doc_metadata["source"],
            'page': doc_metadata["page_number"],
            'title': doc_metadata["filename"],
            'language' : doc_metadata["languages"],
            'author': self.author, 
            'published_date': '문서가 생성된 날짜와 시간',
            'keywords': '문서의 주제나 핵심 내용을 나타내는 키워드'
        }
        
        return metadata
        
    def _get_chunk(self, txt):
        return self.splitter.split_documents(txt)
        
        
    def _insert_to_database(self, docs) -> None:
        self.vs.add_documents(docs)