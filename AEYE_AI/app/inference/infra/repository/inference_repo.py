from fastapi import HTTPException

from database import SessionLocal_mysql
from inference.domain.infer_result import InferenceResult as InferenceResultV0
from inference.domain.repository.result_repo import IInferenceResultRepository
from inference.infra.db_model.result import InferenceResult
from utils.db_utils import row_to_dict


class InferenceRepository(IInferenceResultRepository):
    
    def save(self, result : InferenceResultV0):
        
        new_result = InferenceResult(
            job_id=result.job_id,
            result=result.result,
            classification=result.classification,
            created_at=result.created_at,
            updated_at=result.updated_at
        )
        
        # image = Image(
        #     image_path=image.image_path,
        #     created_at=image.created_at,
        #     updated_at=image.updated_at,
        # )
        
        try:
            with SessionLocal_mysql() as db:
                db = SessionLocal_mysql()
                db.add(new_result)
                db.commit()
        finally:
            db.close()
            
    def search_by_job_id(self, job_id):
        
        with SessionLocal_mysql() as db:
            result = db.query(InferenceResult).filter(InferenceResult.job_id == job_id).first()
        
        if not result:
            return None
    
        return InferenceResult(**row_to_dict(result))