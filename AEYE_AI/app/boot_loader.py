from langchain_core.prompts import ChatPromptTemplate

from AEYE.application.AI.inference import InferenceGPU
from AEYE.application.AI.loader import GPUModelLoader
from AEYE.application.AI.models.llm import shutdown_llm
from AEYE.application.AI.registry import llm_register, vision_register
from AEYE.application.logger import AEYE_log
from AEYE.application.process import Process
from AEYE.application.registry import get_cfg
from AEYE_langchain.application.insert import Grobid_Insert_Paper
from AEYE_langchain.application.retrieve import AEYE_langchain_Retreive
from inference.domain.result import Result
from inference.infra.repository.request_repo import RequestRepository
from inference.infra.repository.result_repo import ResultRepository


async def bootstrap():
    cfg = get_cfg()

    registry = {
        "vision_register" : vision_register,
        "llm_register" : llm_register,
    }
    
    repo = {
        "Request" : RequestRepository(),
        "Result" : ResultRepository(),
    }
    
    entity = {
        "Result" : Result
    }
    
    model_loader = GPUModelLoader(cfg, registry, AEYE_log)
    langchain_retrieve = AEYE_langchain_Retreive(model_loader.get_llm(), None, ChatPromptTemplate)
    Grobid_Insert_Paper(logger=AEYE_log)
    
    inference_gpu = InferenceGPU(model_loader, cfg, langchain_retrieve)
    gpu = Process(cfg, inference_gpu, repo, entity, AEYE_log)

    return gpu
    
    
async def shutdown():
    
    shutdown_llm()
    
    AEYE_log("Bye")