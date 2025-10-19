import time
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Request, UploadFile

from AEYE.application.process import Process
from AEYE.application.registry import get_cfg
from inference.application.router.parser import RequestParser

router = APIRouter()
AEYE_cfg = get_cfg()


def get_parser():
    return RequestParser(AEYE_cfg.HTTP)

def get_Process():
    return Process.get_instance()


@router.post("/inference")
async def inference(request: Request, files: Optional[List[UploadFile]] = File(None),
                    http = Depends(get_parser), gpu = Depends(get_Process)):
    
    job_id = f"{int(time.time() * 1000)}"  # ms 단위

    dataset = await http.get_tensor(request, files)
    await gpu.enqueue_request({"img": dataset, "job_id": job_id})   

    return {
                "status" : "SUCCESS",
                "job_id" : job_id,
            }