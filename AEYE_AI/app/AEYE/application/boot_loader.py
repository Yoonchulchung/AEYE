from AEYE.application.AI.inference import InferenceGPU
from AEYE.application.AI.loader import GPUModelLoader
from AEYE.application.AI.models.llm import shutdown_llm
from AEYE.application.AI.registry import llm_register, vision_register, vlm_register
from AEYE.application.logger import AEYE_log
from AEYE.application.process import Process
from AEYE.application.registry import get_cfg
from AEYE_langchain.langchain import init_langchain
from AEYE_langchain.search import AEYE_langchain_search

llm_model = None
vision_model = None

async def bootstrap():
    global llm_model, vision_model
    cfg = get_cfg()

    init_langchain()

    registry = {
        "vision_register" : vision_register,
        "llm_register" : llm_register,
    }
    model_loader = GPUModelLoader(cfg, registry, AEYE_log)
    aeye_inference = InferenceGPU(model_loader, cfg, AEYE_langchain_search.get_instance())
    
    gpu = Process(cfg, aeye_inference, AEYE_log)

    return gpu
    
    
async def shutdown():
    global llm_model, vision_model
    
    shutdown_llm()
    
    AEYE_log("Bye")