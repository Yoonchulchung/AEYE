from fastapi import HTTPException

from database import SessionLocal_mysql
from inference.domain.repository.request_repo import IRequestRepository
from inference.infra.db_model.request import Request
from utils.db_utils import row_to_dict

from datetime import datetime
from torchvision import transforms
import torch

import os

class RequestRepository(IRequestRepository):
    
    def save(self, image : torch.Tensor, job_id : str):
        
        if not isinstance(image, torch.Tensor):
            raise ValueError(f"Wrong type of image is inserted to Request Repo. ")
        
        if not os.path.isdir("images"):
            os.mkdir("images")
            
        save_path = f"images/{job_id}.jpg"
        img_tensor = image.squeeze(0)
        to_pil = transforms.ToPILImage()
        img_pil = to_pil(img_tensor)
        img_pil.save(save_path)

        now = datetime.now()
        new_request = Request(
            img_path=save_path,
            job_id=job_id,
            created_at=now,
            updated_at=now,
        )
        
        try:
            with SessionLocal_mysql() as db:
                db = SessionLocal_mysql()
                db.add(new_request)
                db.commit()
        finally:
            db.close()
            
    def search_by_job_id(self, job_id):
        
        with SessionLocal_mysql() as db:
            result = db.query(Request).filter(Request.job_id == job_id).first()
        
        if not result:
            return None
    
        return Request(**row_to_dict(result))