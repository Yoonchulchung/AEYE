from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class Paper:
    title : str
    authors : List[str]
    published : datetime
    abstract : str
    language : str
    keywords : List[str]
    category : List[str]
    

@dataclass
class PaperChunk:
    chunk_index : int
    section_title : str
    char_start : str
    char_end : str
    content : str
    embedding : List[float]