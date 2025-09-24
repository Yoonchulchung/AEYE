from AEYE.logger import print_log
from AEYE.inference import AEYE_Inference
from AEYE.AI.loader import GPUModelLoader
from AEYE.process import ProcessGPU
from AEYE.registry import get_cfg

async def bootstrap():
    cfg = get_cfg()
    model_loader = GPUModelLoader(cfg)

    llm_model = model_loader.get_model("gpt-4o-mini", 0)
    vision_model = model_loader.get_model('octdl', 0)
    aeye_inference = AEYE_Inference(vision_model, llm_model)
    
    gpu = ProcessGPU(cfg.Vision_AI, cfg.HTTP, aeye_inference, print_log)
    
    return gpu
    
    
async def shutdown():
    ...