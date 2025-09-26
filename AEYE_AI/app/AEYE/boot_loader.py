from AEYE.AI.inference import AEYE_Inference
from AEYE.AI.loader import GPUModelLoader
from AEYE.AI.registry import llm_register, vision_register, vlm_register
from AEYE.logger import AEYE_log
from AEYE.process import ProcessGPU
from AEYE.registry import get_cfg


async def bootstrap():
    cfg = get_cfg()
    model_loader = GPUModelLoader(cfg, 
                                  vision_register=vision_register,
                                  vlm_register=vlm_register, 
                                  llm_register=llm_register,
                                  logger=AEYE_log)

    llm_model = await model_loader.get_model("LLaMA2", 0)
    vision_model = await model_loader.get_model('OCTDL', 0)
    aeye_inference = AEYE_Inference(vision_model, llm_model)
    
    gpu = ProcessGPU(cfg.Vision_AI, cfg.HTTP, aeye_inference, AEYE_log)
    
    return gpu
    
    
async def shutdown():
    AEYE_log("Bye")