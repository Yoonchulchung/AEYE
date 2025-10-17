from typing import List, Optional

from fastapi import APIRouter, Depends, File, Request, UploadFile

from AEYE.application.process import ProcessGPU
from AEYE.application.registry import get_cfg
from inference.application.router.http_1_1 import Response_HTTP_1_1
import time

router = APIRouter()
AEYE_cfg = get_cfg()


def get_HTTP_parser():
    return Response_HTTP_1_1(AEYE_cfg.HTTP)

def get_ProcessGPU():
    return ProcessGPU.get_instance()

@router.post("/upload/tensor")
async def upload_http_1_1(request : Request, files: Optional[List[UploadFile]] = File(None), 
                 http = Depends(get_HTTP_parser), gpu = Depends(get_ProcessGPU)):
    '''
    Please send bytes data. Do not send Pytorch Tensor format.
    '''
    job_id = f"{int(time.time() * 1000)}"  # ms 단위

    dataset = await http.get_tensor(request, files)
    await gpu.enqueue_batch_or_tensor(dataset)   

    return {
            "status" : "SUCCESS",
            "job_id" : job_id,
        }



@router.post("/upload/pil")
async def upload_http_1_1(request : Request, files: Optional[List[UploadFile]] = File(None), 
                 http = Depends(get_HTTP_parser), gpu = Depends(get_ProcessGPU)):
    '''
    Please send bytes data. Do not send Pytorch Tensor format.
    '''
    job_id = f"{int(time.time() * 1000)}"  # ms 단위

    dataset = await http.get_pil(request, files)
    await gpu.enqueue_batch({"img": dataset, "job_id": job_id})   

    return {
                "status" : "SUCCESS",
                "job_id" : job_id,
            }

