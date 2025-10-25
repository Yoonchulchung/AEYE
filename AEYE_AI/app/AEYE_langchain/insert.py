import re
import os
from abc import ABC, abstractmethod
from typing import Callable, List

from langchain.text_splitter import SpacyTextSplitter
from langchain_core.documents import Document
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_postgres.vectorstores import PGVector
import requests
from tika import parser as TikaParser
from bs4 import BeautifulSoup

class AEYE_Langchain_Insert(ABC):
    '''
    Vectorstore DB에 저장할 PDF 문서 처리를 관리합니다. 
    
    아래와 같은 파이프라인으로 문서를 처리합니다.
    PDF 전처리 -> PDF 로드 -> 텍스트 추출 -> 텍스트 전처리 -> 청크 분할 -> DB 저장
    
    '''
    @abstractmethod
    def _preprocess_pdf(self, pdf_path : str) -> dict:
        '''
        먼저, PDF가 이미지 기반인지 확인합니다. OCR 사용 여부를 체크합니다.
        아래와 같은 메타 정보를 반환합니다.

        {
            "title": 문서의 제목,
            "authors": [문서의 저자명],
            "published": 문서 발행 일자,
            "language": 문서 언어,
            "category": 문서의 카테고리,
            "keywords": 문서 키워드,
        }
        
        정갈된 전처리를 위해 추출된 PDF 제목을 파일 명으로 변경합니다.
        ex :) Attention_is_all_you_need.pdf
        '''
        raise NotImplementedError
    
    @abstractmethod
    def _get_documents_from_pdf(self, pdf_path : str) -> BeautifulSoup:
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
    def _preprocess_text(self, soup : BeautifulSoup) -> str:
        '''
        RAG 검색에 성능을 하락시키는 불필요한 내용을 제거하고 변경합니다.
        
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
        
        if not os.path.basename(pdf_path).split(".")[-1] == "pdf":
            return
        
        self.logger(f"adding {pdf_path} to pgvector...")
        metadata = self._preprocess_pdf(pdf_path)
        # soup = self._get_documents_from_pdf(pdf_path)
        # text = self._preprocess_text(soup)
    
        # chunks = self._get_chunk(soup)
        #self._insert_to_database(text)
        
        #self.logger(f"succeed to add {pdf_path}")

class Grobid_Insert_Paper(AEYE_Langchain_Insert):
    preprocess_pdf_prompt = """
    You are an expert academic researcher skilled at parsing document information.
    Your task is to extract the main category and keywords from the text of the first page of a research paper provided below.

    Follow these rules carefully:
    1. categorize the given document text into a single word. 
    2. Extract keywords that describes the given document text well. There should be five keywords.
    3. Format your response as a valid JSON object with two keys: "category" and "keywords".
    4. The value for "category" must be a string and lowercase.
    5. The value for "keywords" must be a list of strings and lowercase.
    6. Do NOT add any introductory text, explanations, or markdown formatting like ```json. Your response must be ONLY the raw JSON object.
    
    ## JSON Output Format
    {{
    "category": "<Your generated concise category>",
    "keywords": "<Your generated concise keywords>",
    }}
    
    ---
    DOCUMENT TEXT:
    {abstract}
    ---

    JSON OUTPUT:
    """
    
    name_prompt = """
    You are an expert academic researcher with a talent for abstraction and distillation.
    Your task is to create a concise, alternative title for a research paper by analyzing its original title and abstract. The new title must capture the core subject and contribution of the paper.

    ## Rules
    1.  Read the provided TITLE and ABSTRACT to understand the paper's main theme.
    2.  Generate a new, shorter title that is clear, descriptive, and easy to understand.
    3.  Your output MUST be a single, raw JSON object. Do NOT include any explanations, introductory text, or markdown formatting like ```json.

    ## JSON Output Format
    {{
    "title": "<Your generated concise title>"
    }}

    ## Example
    ---
    ### INPUT:
    - **TITLE**: "An Attention-Based Bidirectional Long Short-Term Memory Network with a Convolutional Neural Network for Sentence-Level Text Classification"
    - **ABSTRACT**: "This paper proposes a novel deep learning model for sentence-level text classification. We combine a Convolutional Neural Network (CNN) to extract local features from words with a Bidirectional Long Short-Term Memory (Bi-LSTM) network to capture long-range dependencies. Furthermore, we introduce an attention mechanism that allows the model to focus on the most relevant parts of the sentence when making a prediction. Our experiments on several benchmark datasets show that the proposed model significantly outperforms previous state-of-the-art methods in accuracy and F1 score."

    ### EXPECTED JSON OUTPUT:
    {{
    "title": "Attention-based Bi-LSTM with CNN for Text Classification"
    }}
    ---

    ## Your Task
    ---
    ### INPUT:
    - **TITLE**: "{title}"
    - **ABSTRACT**: "{abstract}"

    ### JSON OUTPUT:
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
        
        #llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
        self.llm = ChatOllama(model="llama3", temperature=0)
        self.string_parser = JsonOutputParser()

        self.vs = vs
        self.logger = logger
        
        self.GROID_HEADER_URL = "http://localhost:8070/api/processHeaderDocument"
        self.GROBID_FULL_URL = "http://localhost:8070/api/processFulltextDocument"


    def _preprocess_pdf(self, pdf_path : str) -> dict:
        
        parsed = TikaParser.from_file(pdf_path)
        metadata = parsed["metadata"]
        
        with open(pdf_path, "rb") as f:
            response = requests.post(self.GROID_HEADER_URL, files={"input": f})
        
        soup = BeautifulSoup(response.text, "xml")
        title = soup.find("title").get_text(strip=True)
        
        analytic = soup.find("analytic")
        authors = analytic.find_all("author")
        
        names = []
        for author in authors:
            pers = author.find("persName")
            if pers:
                forenames = [f.get_text(strip=True) for f in pers.find_all("forename")]
                surname = pers.find("surname")
                surname_text = surname.get_text(strip=True) if surname else ""
                full_name = " ".join(forenames + [surname_text])
                names.append(full_name)
                
        lang = soup.find("text").get("xml:lang")
        abstract = soup.find("abstract").get_text(strip=True)
                
        def _save_renamed_file(pdf_path, soup):
            
            directory = os.path.dirname(pdf_path)
            new_filename = title.replace(" ", "_").lower()
            
            if len(new_filename) > 10:
                prompt = ChatPromptTemplate.from_template(template=self.name_prompt)
                chain = prompt | self.llm | self.string_parser
                name = chain.invoke({"abstract": abstract,"title" : new_filename})
                new_filename = name["title"]
            
            new_path = os.path.join(directory, new_filename)
            new_pdf_path = new_path + ".pdf"
            
            os.rename(pdf_path, new_pdf_path)
        
            return new_path
        
        new_path = _save_renamed_file(pdf_path, soup)
        prompt = ChatPromptTemplate.from_template(template=self.preprocess_pdf_prompt)
        chain = prompt | self.llm | self.string_parser
        result = chain.invoke({"abstract": abstract})
        
        payload = {
            "title": title,
            "authors": names,
            "published": metadata["pdf:docinfo:created"],
            "language": lang,
            "category": result["category"],
            "keywords": result["keywords"],
        }
        
        def _save_meta_info(new_path, payload):
            
            new_path_meta = new_path + "_meta.md"

            with open(new_path_meta, "w") as w:
                w.write(str(payload))
        
        _save_meta_info(new_path, payload)
        
        return payload
    
    
    def _get_documents_from_pdf(self, pdf_path : str) -> BeautifulSoup:
        
        with open(pdf_path, "rb") as f:
            response = requests.post(self.GROBID_FULL_URL, files={"input": f})        
            
        soup = BeautifulSoup(response.text, "xml")
        
        
        
        return soup
    
        
    def _preprocess_text(self, soup : BeautifulSoup) -> str:
        
        texts = soup.find("body").get_text(strip=True)
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
        
    def _get_chunk(self, soup : BeautifulSoup):
        context_chunks = []
        
        sections = soup.find("body")
                    
    def _insert_to_database(self, context_chunks, ) -> None:
        
        docs = [
            Document(page_content=text, metadata=...)
            for i, text in enumerate(context_chunks)
        ]
        
        
        self.vs.add_documents(docs)