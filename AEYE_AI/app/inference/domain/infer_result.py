from dataclasses import dataclass
from datetime import datetime


@dataclass
class Image:
    image_path : str
    
@dataclass
class InferenceResult:
    job_id : str
    result : str
    classification : str