import time
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Request, UploadFile

from AEYE.application.process import Process
from AEYE.application.registry import get_cfg
from inference.application.router.parser import RequestParserTensor
from fastapi.responses import JSONResponse

router = APIRouter()
AEYE_cfg = get_cfg()


def get_parser():
    return RequestParserTensor(AEYE_cfg.HTTP)

def get_Process():
    return Process.get_instance()


@router.post("/inference")
async def inference(request: Request, files: Optional[List[UploadFile]] = File(None),
                    http = Depends(get_parser), gpu = Depends(get_Process)):
    '''
    이미지를 업로드하면 job id를 할당받게 됩니다.
    할당받은 job id를 이용하여 /api/v1/result/{job_id}로 추론 결과를 확인해주세요.
    최대 5초 정도 추론 시간이 필요합니다.
    허용되는 Content-type은 아래와 같아요.
    
        - multipart/form-data
        - application/octet-stream
        - application/json
        - application/x-www-form-urlencoded
    
    '''
    
    job_id = f"{int(time.time() * 1000)}"  # ms 단위
    
    try:
        dataset = await http.get_img(request, files)
        await gpu.enqueue_request({"img": dataset, "job_id": job_id})   
        payload = {
            "status" : "SUCCESS",
            "job_id" : job_id,
        }
        status_code = 200
    except Exception as e:
        payload = {
            "status" : "FAILED",
            "message" : str(e),
        }
        status_code = 400
        
        
    return JSONResponse(status_code=status_code, content=payload)