from fastapi import APIRouter

from inference.infra.repository.result_repo import ResultRepository

router = APIRouter()

@router.get("/inference/result/{job_id}")
async def inference_result(job_id: str):
    '''
    /api/v1/inference 에서 할당 받은 job id를 이용하여 결과를 확인하세요.
    '''

    repo = ResultRepository()
    result = repo.search_by_job_id(job_id)
    
    if result is not None:
        payload = {
            "status" : "SUCCESS",
            "job_id" : job_id,
            "classification" : result.classification,
            "result" : result.result,
        }
    else:
        payload = {
            "status" : "WAIT"
        }
    
    return payload
    