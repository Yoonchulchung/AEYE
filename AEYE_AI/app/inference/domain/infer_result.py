from dataclasses import dataclass
from datetime import datetime


@dataclass
class Image:
    image_path : str
    created_at : datetime
    updated_at : datetime
    
@dataclass
class InferenceResult:
    job_id : str
    result : str
    classification : str
    created_at : datetime
    updated_at : datetime