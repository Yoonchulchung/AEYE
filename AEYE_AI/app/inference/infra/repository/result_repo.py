from fastapi import HTTPException

from database import SessionLocal_mysql
from inference.domain.result import Result as ResultV0
from inference.domain.repository.result_repo import IResultRepository
from inference.infra.db_model.result import Result
from utils.db_utils import row_to_dict

from datetime import datetime


class ResultRepository(IResultRepository):
    
    def save(self, result : ResultV0):
        
        now = datetime.now()
        new_result = Result(
            job_id=result.job_id,
            classification=result.classification,
            result=result.result,
            result_summary=result.result_summary,
            created_at=now,
            updated_at=now,
        )
        
        try:
            with SessionLocal_mysql() as db:
                db = SessionLocal_mysql()
                db.add(new_result)
                db.commit()
        finally:
            db.close()
            
    def search_by_job_id(self, job_id):
        
        with SessionLocal_mysql() as db:
            result = db.query(Result).filter(Result.job_id == job_id).first()
        
        if not result:
            return None
    
        return Result(**row_to_dict(result))