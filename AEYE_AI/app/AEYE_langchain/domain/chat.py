from dataclasses import dataclass
from typing import Dict


@dataclass
class Chat:
    title : str
    metadata : Dict[str, str]
    
@dataclass
class Message:
    role : str
    content : str
    metadata : Dict[str, str]
    