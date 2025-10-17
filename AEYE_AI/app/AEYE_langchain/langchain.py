from AEYE_langchain.application.database import AEYE_Langchain_DB
from AEYE_langchain.application.search import AEYE_langchain_search
from AEYE_langchain.application.insert import AEYE_Langchain_insert
from AEYE_langchain.application.model import AEYE_Langchain_Model
from AEYE_langchain.application.logger import AEYE_LC_log
from AEYE.application.registry import get_cfg

def init_langchain():
    
    AEYE_LC_log("Initiating AEYE Langchain...")
    
    aeye_cfg = get_cfg()
    model = AEYE_Langchain_Model(aeye_cfg.langchain)
    vectorstore = AEYE_Langchain_DB(aeye_cfg.langchain)
    
    AEYE_langchain_search(
        llm=model.get_llm(),
        retriever=vectorstore.get_retriever(),
        prompt=model.get_prompt()
    )
    
    AEYE_Langchain_insert(
        vs=vectorstore.get_vectorstore(),
        logger=AEYE_LC_log,
    )
    
    AEYE_LC_log("Initiating AEYE Langchain is completed!")