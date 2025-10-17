from AEYE.application.AI.inference import AEYE_Inference
from AEYE.application.AI.loader import GPUModelLoader
from AEYE.application.AI.models.llm import shutdown_llm
from AEYE.application.AI.registry import llm_register, vision_register, vlm_register
from AEYE.application.logger import AEYE_log
from AEYE.application.process import ProcessGPU
from AEYE.application.registry import get_cfg

from AEYE_langchain.application.langchain import init_langchain
from AEYE_langchain.application.search import AEYE_langchain_search
llm_model = None
vision_model = None

async def bootstrap():
    global llm_model, vision_model
    cfg = get_cfg()

    init_langchain()

    model_loader = GPUModelLoader(cfg, 
                                  vision_register=vision_register,
                                  vlm_register=vlm_register, 
                                  llm_register=llm_register,
                                  logger=AEYE_log)
    llm_model = await model_loader.get_model("Qwen2", 0)
    vision_model = await model_loader.get_model('OCTDL', 0)

    aeye_inference = AEYE_Inference(vision_model, llm_model, cfg, AEYE_langchain_search.get_instance())
    
    gpu = ProcessGPU(cfg.Vision_AI, cfg.HTTP, aeye_inference, AEYE_log)
    
    
    return gpu
    
    
async def shutdown():
    global llm_model, vision_model
    
    shutdown_llm()
    
    AEYE_log("Bye")