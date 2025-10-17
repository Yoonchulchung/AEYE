import base64
import io

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from PIL import Image

from AEYE.application.process import ProcessGPU

router = APIRouter()

@router.get("/result/{job_id}")
async def inference_result(job_id: str):
    gpu = ProcessGPU.get_instance()
    
    status = await gpu.get_status(job_id)
