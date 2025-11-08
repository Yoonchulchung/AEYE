from typing import List

from sqlalchemy.orm import Session

from AEYE_langchain.domain.insert import Paper as PaperV0
from AEYE_langchain.infra.db_model.insert import Paper, PaperChunk


def insert_paper_and_chunks(session: Session, paper : PaperV0, chunks : List) :
    
    new_paper = Paper(
        title     = paper.title,
        authors   = paper.authors,
        published = paper.published,
        abstract  = paper.abstract,
        language  = paper.language,
        keywords  = paper.keywords,
        category  = paper.category,
    )
    
    for chunk in chunks:
        new_chunk = PaperChunk(
            chunk_index   = chunk[0],
            section_title = chunk[1],
            char_start    = chunk[2],
            char_end      = chunk[3],
            content       = chunk[4],
            embedding     = chunk[5],
        )
        new_paper.chunks.append(new_chunk)    
        
    try:
        session.add(new_paper)
        session.commit()
    except Exception as e:
        
        session.rollback()
        print(f"Something wrong while inserting paper with ORM: {e}")
        raise e