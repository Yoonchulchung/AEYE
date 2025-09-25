from AEYE.logger import AEYE_log
from AEYE.inference import AEYE_Inference
from AEYE.AI.loader import GPUModelLoader
from AEYE.process import ProcessGPU
from AEYE.registry import get_cfg
from AEYE.AI.registry import vlm_register, vision_register


async def bootstrap():
    cfg = get_cfg()
    model_loader = GPUModelLoader(cfg, 
                                  vision_register=vision_register, 
                                  vlm_register=vlm_register, 
                                  logger=AEYE_log)

    #llm_model = await model_loader.get_model("gpt-4o-mini", 0)
    llm_model = None
    vision_model = await model_loader.get_model('octdl', 0)
    aeye_inference = AEYE_Inference(vision_model, llm_model)
    
    gpu = ProcessGPU(cfg.Vision_AI, cfg.HTTP, aeye_inference, AEYE_log)
    
    return gpu
    
    
async def shutdown():
    ...