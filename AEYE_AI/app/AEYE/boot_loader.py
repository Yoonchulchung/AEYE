from AEYE.AI.models.octdl import generate_model
from AEYE.inference import AEYE_Inference
from AEYE.AI.loader import GPUModelLoader
from AEYE.registry import get_cfg

async def bootstrap():
    cfg = get_cfg()
    model_loader = GPUModelLoader(cfg)

    llm_model = model_loader.get_model("gpt-4o-mini")
    vision_model = model_loader.get_model('octdl')
    aeye_inference = AEYE_Inference(vision_model, llm_model)
    
    
    
    
    
async def shutdown():
    ...