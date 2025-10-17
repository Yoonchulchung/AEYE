from dataclasses import dataclass
from datetime import datetime


@dataclass
class Image:
    image_path : str
    created_at : datetime
    updated_at : datetime
    
@dataclass
class Result:
    job_id : str
    result : str
    created_at : datetime
    updated_at : datetime