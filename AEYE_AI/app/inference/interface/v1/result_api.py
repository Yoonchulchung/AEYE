from fastapi import APIRouter

from inference.infra.repository.inference_repo import InferenceRepository

router = APIRouter()

@router.get("/inference/result/{job_id}")
async def inference_result(job_id: str):

    repo = InferenceRepository()
    result = repo.search_by_job_id(job_id)
    
    payload = {
        "job_id" : job_id,
        "classification" : result.classification,
        "result" : result.result,
    }
    
    return payload
    