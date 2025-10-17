from AEYE_langchain.application.database import AEYE_Langchain_DB
from AEYE_langchain.application.search import AEYE_langchain_search
from AEYE_langchain.application.insert import AEYE_Langchain_insert
from AEYE_langchain.application.model import AEYE_Langchain_Model
from AEYE_langchain.application.logger import AEYE_LC_log

def init_langchain():
    
    AEYE_LC_log("Initiating AEYE Langchain...")
    model = AEYE_Langchain_Model()
    vectorstore = AEYE_Langchain_DB()
    
    search = AEYE_langchain_search(
        llm=model.get_llm(),
        retriever=vectorstore.get_retriever(),
        prompt=model.get_prompt(),
    )
    
    insert = AEYE_Langchain_insert(
        vs=vectorstore.get_vectorstore(),
        logger=AEYE_LC_log,
    )
    
    AEYE_LC_log("Initiating AEYE Langchain is completed!")