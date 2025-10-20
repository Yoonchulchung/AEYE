from dataclasses import dataclass


@dataclass
class Request:
    job_id : str
    image_path : str