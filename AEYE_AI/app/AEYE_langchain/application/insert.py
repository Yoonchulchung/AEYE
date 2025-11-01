import os
import re
from abc import ABC, abstractmethod
from typing import Callable, Dict, List

import requests
from bs4 import BeautifulSoup
from langchain.docstore.document import Document
from langchain.text_splitter import SpacyTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_ollama import ChatOllama
from tika import parser as TikaParser

from AEYE_langchain.domain.insert import Paper
from AEYE_langchain.infra.repository.insert import insert_paper_and_chunks
from database import SessionLocal

from .prompt import name_prompt, preprocess_pdf_prompt


class AEYE_Langchain_Insert(ABC):
    '''
    Vectorstore DB에 저장할 PDF 문서 처리를 관리합니다. 
    
    아래와 같은 파이프라인으로 문서를 처리합니다.
    PDF 전처리 -> PDF 로드 -> 텍스트 추출 -> 텍스트 전처리 -> 청크 분할 -> DB 저장
    
    '''
    @abstractmethod
    def _preprocess_pdf(self, pdf_path : str) -> Dict:
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
    def _get_documents_from_pdf(self, pdf_path : str) -> str:
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
    def _preprocess_text(self, sections_list : List, pdf_path : str) -> List:
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
    def _get_chunks(self, sections : List) -> List:
        '''
        추출된 데이터에서 아래와 같이 청크 데이터를 만듭니다.
        [
            "chunk_index", 
            "section_title",
            "char_start",
            "char_end",
            "content",
            "embedding",
        ]
        '''
        raise NotImplementedError
        
    @abstractmethod
    def _insert_to_database(self, meta_data : Dict, chunks : List) -> None:
        '''
        문서를 DB에 저장합니다.
        '''
        raise NotImplementedError
    
    def add_pdf(self, pdf_path : str) -> None:
        
        if not os.path.exists(pdf_path):
            raise ValueError(f"Wrong path : {pdf_path}")
        
        if not os.path.basename(pdf_path).split(".")[-1] == "pdf":
            return
        
        self.logger(f"adding {pdf_path} to DB...")
        
        metadata, new_path = self._preprocess_pdf(pdf_path)
        sections           = self._get_documents_from_pdf(new_path)
        text               = self._preprocess_text(sections, new_path)
        chunks             = self._get_chunks(text)
        self._insert_to_database(metadata, chunks)
        self.logger(f"succeed to add {pdf_path}")
        return chunks


class Grobid_Insert_Paper(AEYE_Langchain_Insert):
    
    def __init__(
        self, 
        chunk_size : int = 1000, 
        chunk_overlap : int = 100,
        logger : Callable = None,
        neo4jgraph = None,
        ):
        
        self.splitter = SpacyTextSplitter(chunk_size=chunk_size,
                                          chunk_overlap=chunk_overlap)
        
        #llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
        self.llm = ChatOllama(model="llama3", temperature=0)
        
        self.llm_transformer = LLMGraphTransformer(llm=self.llm)
        self.neo4jgraph = neo4jgraph
        
        self.output_parser = JsonOutputParser()

        self.name_prompt_temp = ChatPromptTemplate.from_template(template=name_prompt)
        self.name_chain = self.name_prompt_temp | self.llm | self.output_parser
                
        self.pdf_prompt = ChatPromptTemplate.from_template(template=preprocess_pdf_prompt)
        self.result_chain = self.pdf_prompt | self.llm | self.output_parser
        
        self.logger = logger
        
        self.GROID_HEADER_URL = "http://localhost:8070/api/processHeaderDocument"
        self.GROBID_FULL_URL = "http://localhost:8070/api/processFulltextDocument"

        self.embedding_model = SentenceTransformerEmbeddings(
                                    model_name="intfloat/multilingual-e5-base"
                                )

    def _preprocess_pdf(self, pdf_path : str) -> Dict:
        
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
                
        def _save_renamed_file(pdf_path : str, title : str) -> None:
                        
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
        
        def _save_meta_info(new_path : str, payload : Dict) -> None:
            
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
    
        
    def _preprocess_text(self, sections_list : List, pdf_path : str) -> List:
        
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
        
    
    def _get_chunks(self, sections : List) -> List:
        
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
                    
                    
    def _insert_to_database(self, meta_data : Dict, chunks : List) -> None:
        
        #save_to_postgresql(meta_data, chunks)
        save_to_neo_4j(self.llm_transformer, chunks, self.neo4jgraph)
        
        
def save_to_postgresql(meta_data, chunks):
                
    paper = Paper(
        title=meta_data['title'],
        authors=meta_data['authors'],
        published=meta_data['published'],
        abstract=meta_data['abstract'],
        language=meta_data['language'],
        keywords=meta_data['keywords'],
        category=meta_data['category']
    )
    
    with SessionLocal() as session:
        insert_paper_and_chunks(session, paper, chunks)
        
        
def save_to_neo_4j(llm_transformer, chunks, neo4jgraph):
    
    print("===========================")
    print("saving to neo4j...")    
    documents = [Document(page_content=chunk[4]) for chunk in chunks]
    graph_documents = llm_transformer.convert_to_graph_documents(documents)
    
    print(graph_documents)
    neo4jgraph.add_graph_documents(
        graph_documents,
        baseEntityLabel=True,
    )
    
    node_count_query = """
        MATCH (n)
        RETURN count(n) AS TotalNodes"""
    node_result = neo4jgraph.query(node_count_query)
    print(node_result)
    
    print("===========================")
    