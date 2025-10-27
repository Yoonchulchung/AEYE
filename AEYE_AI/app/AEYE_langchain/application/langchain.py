from AEYE.application.registry import get_cfg
from .insert import Grobid_Insert_Paper
from .logger import AEYE_LC_log
from .search import AEYE_langchain_search


def init_langchain():
    
    AEYE_LC_log("Initiating AEYE Langchain...")
    
    aeye_cfg = get_cfg()
    
    AEYE_langchain_search(
        llm=...,
        retriever=...,
        prompt=...
    )
    
    Grobid_Insert_Paper(
        logger=AEYE_LC_log,
    )
    
    AEYE_LC_log("Initiating AEYE Langchain is completed!")