import os
import re
from abc import ABC, abstractmethod
from typing import Callable

import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import SpacyTextSplitter
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain.docstore.document import Document
from tika import parser as TikaParser

from database import connection_pool
from langchain_community.embeddings import SentenceTransformerEmbeddings

from .query import create_table, insert_paper, insert_paper_chunk


class AEYE_Langchain_Insert(ABC):
    '''
    Vectorstore DB에 저장할 PDF 문서 처리를 관리합니다. 
    
    아래와 같은 파이프라인으로 문서를 처리합니다.
    PDF 전처리 -> PDF 로드 -> 텍스트 추출 -> 텍스트 전처리 -> 청크 분할 -> DB 저장
    
    '''
    @abstractmethod
    def _preprocess_pdf(self, pdf_path : str) -> dict:
        '''
        아래와 같은 메타 정보를 반환합니다.

        {
            "title": 문서의 제목,
            "authors": [문서의 저자명],
            "published": 문서 발행 일자,
            "abstract": 문서 요약문,
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
    def _get_chunks(self, text):
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
        metadata, new_path = self._preprocess_pdf(pdf_path)
        sections = self._get_documents_from_pdf(new_path)
        text = self._preprocess_text(sections, new_path)
        chunks = self._get_chunks(text)
        self._insert_to_database(metadata, chunks)
        self.logger(f"succeed to add {pdf_path}")

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
        chunk_size : int = 1000, 
        chunk_overlap : int = 100,
        logger : Callable = None
        ):
        
        self.splitter = SpacyTextSplitter(chunk_size=chunk_size,
                                          chunk_overlap=chunk_overlap)
        
        #llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
        self.llm = ChatOllama(model="llama3", temperature=0)
        self.output_parser = JsonOutputParser()

        self.name_prompt_temp = ChatPromptTemplate.from_template(template=self.name_prompt)
        self.name_chain = self.name_prompt_temp | self.llm | self.output_parser
                
        self.pdf_prompt = ChatPromptTemplate.from_template(template=self.preprocess_pdf_prompt)
        self.result_chain = self.pdf_prompt | self.llm | self.output_parser
        
        self.logger = logger
        
        self.GROID_HEADER_URL = "http://localhost:8070/api/processHeaderDocument"
        self.GROBID_FULL_URL = "http://localhost:8070/api/processFulltextDocument"

        conn = None
        try:
            conn = connection_pool.getconn()
            create_table(conn)
            conn.commit()
        
        except Exception as e:
            conn.rollback()
            print(f"Something wrong while creating table : {e}")
            
        finally:
            if conn:
                connection_pool.putconn(conn)

        self.embedding_model = SentenceTransformerEmbeddings(
                                    model_name="intfloat/multilingual-e5-base"
                                )

    def _preprocess_pdf(self, pdf_path : str) -> dict:
        
        parsed = TikaParser.from_file(pdf_path)
        metadata = parsed['metadata']
        
        with open(pdf_path, "rb") as f:
            response = requests.post(self.GROID_HEADER_URL, files={"input": f})
            response.raise_for_status()
        
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
                
        def _save_renamed_file(pdf_path : str, title : str):
                        
            if len(title) > 50:
                name = self.name_chain.invoke({'abstract': abstract, 'title': title})
                title = str(name['title'])
            
            new_filename = title.replace(" ", "_").lower()
            
            directory = os.path.dirname(pdf_path)
            new_pdf_path = os.path.join(directory, new_filename) + ".pdf"
            os.rename(pdf_path, new_pdf_path)
        
            return new_pdf_path
        
        new_path = _save_renamed_file(pdf_path, title)
        result = self.result_chain.invoke({"abstract": abstract})
        
        payload = { 
                    "title": title,
                    "authors": names,
                    "abstract": abstract,
                    "published": metadata["pdf:docinfo:created"],
                    "language": lang,
                    "category": result['category'],
                    "keywords": result['keywords'],
                  }
        
        def _save_meta_info(new_path : str, payload):
            
            root, ext = os.path.splitext(new_path)
            new_path_meta = root + "_meta.md"
            with open(new_path_meta, "w") as w:
                w.write(str(payload))
        
        _save_meta_info(new_path, payload)
        
        return payload, new_path
    
    
    def _get_documents_from_pdf(self, pdf_path : str) -> str:
        
        with open(pdf_path, "rb") as f:
            response = requests.post(self.GROBID_FULL_URL, files={"input": f})
            response.raise_for_status()
                
        soup = BeautifulSoup(response.text, "xml")
        body = soup.find("text").find("body") if soup.find("text") else None
        
        sections = []
        if body:
            for div in body.find_all("div", recursive=False):
                head = div.find("head")
                sec_title = head.text.strip() if head else ""
                
                sec_text = " ".join(div.stripped_strings)
                sections.append({"title" : sec_title, "text" : sec_text})
        
        return sections
    
        
    def _preprocess_text(self, sections_list : list, pdf_path : str) -> list:
        
        sections = []
        for paragraph in sections_list:
            sec_title = paragraph['title']
            sec_text = paragraph['text']
            
            # Reference [1, 2] 형태 제거
            sec_text = re.sub(r'\[[\d,\s]+\]', '', sec_text)
            # Fig, Table, Fig, Appendix 제거
            pattern = re.compile(r'(?:Figure|Fig|Table|Appendix)s?\.?\s*[\d\s,-]+', re.IGNORECASE)
            sec_text = pattern.sub('', sec_text)
            
            sec_text = sec_text.replace(sec_title, '', 1).strip()
            sections.append({"title" : sec_title, "text" : sec_text})
        
        def save_body_text():    
            body_text = "\n\n".join(
                [f"{s['title']}\n{s['text']}" if s['title'] else s['text'] for s in sections]
            ).strip()
            
            new_md = os.path.dirname(pdf_path) + "/" + os.path.basename(pdf_path).split(".")[0] + "__.md"
            with open(new_md, "w") as w:
                w.write(str(body_text))    
        save_body_text()
        
        return sections
        
    
    def _get_chunks(self, sections):
        
        chunk_index_counter = 1
        
        pre_embedding_chunks = []
        chunk_contents = []
        for section in sections:
            original_text = section['text']
            
            doc = Document(
                page_content=original_text,
                metadata={
                    'section_title': section['title']
                }
            )
            split_chunks = self.splitter.split_documents([doc])

            for chunk in split_chunks:
                content = chunk.page_content            
                char_start = original_text.find(content)
                
                if char_start == -1:
                    
                    char_start = 0
                    
                char_end = char_start + len(content)
                pre_embedding_chunks.append({
                    "chunk_index": chunk_index_counter,
                    "section_title": chunk.metadata['section_title'],
                    "char_start": char_start,
                    "char_end": char_end,
                    "content": content
                })
                chunk_contents.append(content)
                chunk_index_counter += 1
        if chunk_contents:
            embeddings = self.embedding_model.embed_documents(chunk_contents)
        else:
            return []
        
        final_chunks = []
        
        for chunk_data, embedding in zip(pre_embedding_chunks, embeddings):
            chunk_tuple = (
                chunk_data['chunk_index'],
                chunk_data['section_title'],
                chunk_data['char_start'],
                chunk_data['char_end'],
                chunk_data['content'],
                embedding 
            )
            final_chunks.append(chunk_tuple)
            
        return final_chunks
                    
                    
    def _insert_to_database(self, meta_data, context_chunks) -> None:
        
        conn = None
        try:
            conn = connection_pool.getconn()
            paper_id = insert_paper(
                conn, 
                title=meta_data['title'],
                authors=meta_data['authors'],
                published=meta_data['published'],
                abstract=meta_data['abstract'],
                language=meta_data['language'],
                keywords=meta_data['keywords'],
                category=meta_data['category']
            )
            
                
            for chunk in context_chunks:
                insert_paper_chunk(
                    conn,
                    paper_id=paper_id,
                    chunk_index=chunk[0],
                    section_title=chunk[1],
                    char_start=chunk[2],
                    char_end=chunk[3],
                    content=chunk[4],
                    embedding=chunk[5]
                )
            conn.commit()
            
        except Exception as e:
            if conn:
                conn.rollback()
                print(f"Somethign wrong inserting to database : {e}")
            
            raise e
            
        finally:
            if conn:
                connection_pool.putconn(conn)