from dataclasses import dataclass

    
@dataclass
class Result:
    job_id : str
    classification : str
    result : str
    result_summary : str